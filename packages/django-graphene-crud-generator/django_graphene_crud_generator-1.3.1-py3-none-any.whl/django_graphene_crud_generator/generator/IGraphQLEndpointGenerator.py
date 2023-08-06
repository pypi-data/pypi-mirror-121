import abc
import inspect
import logging
from typing import Dict, Union, Callable, List

import graphene
import graphene_django

from django_koldar_utils.graphql_toolsbox import graphql_decorators
from django_koldar_utils.graphql_toolsbox.graphql_types import TGrapheneInputType, TGrapheneType, TDjangoModelType, \
    TGrapheneQuery, TGrapheneArgument, TGrapheneWholeQueryReturnType

from django_graphene_crud_generator.IGraphQLEndpointComponent import IGraphQLEndpointComponent
from django_graphene_crud_generator.generator.contexts import GraphQLBuildtimeContext, GraphQLRuntimeContext

LOG = logging.getLogger(__name__)


class IGraphQLEndpointGenerator(IGraphQLEndpointComponent, abc.ABC):
    """
    Generate a mutation/query endpoint
    """

    def __init__(self):
        self.components = []

    def register_component(self, *components: any):
        """
        Register a component. A component is an additional class that can be used to agument this generator.
        It is like a mixin, but can be programmatically added and removed as the developer wishes
        :param components: compoenents to register
        """
        for x in components:
            self.components.append(x)

    def clear_components(self):
        self.components.clear()

    @abc.abstractmethod
    def _compute_graphene_class(self, build_context: GraphQLBuildtimeContext) -> type:
        """
        Function used to generate a class that represents a graphene query
        """
        pass

    @abc.abstractmethod
    def graphql_body_function(self, runtime_context: GraphQLRuntimeContext, *args, **kwargs) -> TGrapheneWholeQueryReturnType:
        """
        A function that is called when the graphql endpoint is invoked. The output is the return valu that you want to
        pass to graphene.
        :param runtime_context: information known at runtime
        :param args: graphql arguments
        :param kwargs: graphql arguments
        :return: return value to pass to graphene
        """
        pass

    def generate(self, **kwargs) -> TGrapheneQuery:
        """
        Allows you to create a graphql endpoint in a easy manner

        :param kwargs: parameters implementatio dependent. The user can use these to pass important data to the implementation
        :return: a class representing a callable from graphql
        """
        # @graphql_subquery
        # class Query(graphene_toolbox.ObjectType):
        #     question = graphene_toolbox.Field(
        #         QuestionType,
        #         foo=graphene_toolbox.String(),
        #         bar=graphene_toolbox.Int()
        #     )
        #
        #     def resolve_question(root, info, foo, bar):
        #         # If `foo` or `bar` are declared in the GraphQL query they will be here, else None.
        #         return Question.objects.filter(foo=foo, bar=bar).first()

        build_context = GraphQLBuildtimeContext(
            params=kwargs
        )

        # arguments
        build_context.action_arguments = dict()
        build_context.action_arguments = self._generate_action_arguments(build_context)
        for x in self.components:
            if hasattr(x, "_generate_action_arguments"):
                build_context.action_arguments.update(x._generate_action_arguments(build_context))

        # return type
        build_context.action_return_type = dict()
        build_context.action_return_type = self._generate_action_return_type(build_context)
        for x in self.components:
            if hasattr(x, "_generate_action_return_type"):
                build_context.action_return_type.update(x._generate_action_return_type(build_context))

        # endpoint class name
        build_context.action_class_name = self._generate_action_class_name(build_context)
        for x in self.components:
            if hasattr(x, "_generate_action_class_name"):
                build_context.action_class_name = x._generate_action_class_name(build_context)

        build_context.action_description = []
        build_context.action_description = self._generate_action_description(build_context)
        for x in self.components:
            if hasattr(x, "_generate_action_description"):
                build_context.action_description.extend(x._generate_action_description(build_context))
        build_context.action_description = "\n".join(build_context.action_description)

        assert build_context.action_class_name is not None, "Query class name is None"
        assert all(map(lambda x: x is not None, build_context.action_arguments.keys())), f"Some arguments of {build_context.action_class_name} are None"
        assert build_context.action_return_type is not None, f"return type of {build_context.action_class_name} is None"
        assert build_context.action_description is not None, f"description of {build_context.action_class_name} is None"
        assert (not inspect.isclass(build_context.action_return_type)) or (issubclass(build_context.action_return_type, (graphene.Scalar, graphene.ObjectType, graphene_django.DjangoObjectType))), \
            f"return type \"{build_context.action_return_type}\" of \"{build_context.action_class_name}\" cannot be a type subclass graphene_toolbox.Field, but needs to be a plain ObjectType!"
        assert ((inspect.isclass(build_context.action_return_type)) or (isinstance(build_context.action_return_type, (graphene.List, graphene.Field)))), \
            f"return type \"{build_context.action_return_type}\" of \"{build_context.action_class_name}\" cannot be an instanc deriving graphene_toolbox.Field, but needs to be a plain ObjectType!"

        def perform_query(root, info, *args, **kwargs) -> any:

            nonlocal build_context

            def generator_body_to_graphene_basic_mapper(f):
                def wrapper(aruntime, *aargs, **akwargs):
                    return f(aruntime.root, aruntime.info, *aruntime.args, **aruntime.kwargs)

                return wrapper

            def graphene_basic_to_generator_body_mapper(f):
                def wrapper(acls, ainfo, *aargs, **akwargs):
                    return f(runtime_context, *runtime_context.args, **runtime_context.kwargs)

                return wrapper

            if root is None:
                root = build_context.get_data("query_class")

            runtime_context = GraphQLRuntimeContext(build_context, root, info, *args, **kwargs)
            LOG.info(f"Computing result for graphql query {build_context.action_class_name}...")

            body = self.graphql_body_function
            body = self._graphql_body_function_decorator(body, runtime_context)
            for x in self.components:
                if hasattr(x, "_graphql_body_function_decorator_native"):
                    # _graphql_body_function_decorator_native returns a GrapheneBodyFunction, not a GrapheneGeneratorBodyFunction
                    # so we need to a mapper
                    body = generator_body_to_graphene_basic_mapper(body)
                    body = x._graphql_body_function_decorator_native(body, runtime_context)
                    body = graphene_basic_to_generator_body_mapper(body)
                elif hasattr(x, "_graphql_body_function_decorator"):
                    body = x._graphql_body_function_decorator(body, runtime_context)
            result = body(runtime_context, *args, **kwargs)

            LOG.info(f"returning to graphene as the request {root} the value {result} (type {type(result)})")
            return result

        build_context.action_body = perform_query

        result_class = self._compute_graphene_class(build_context)
        build_context.action_class = result_class
        return result_class
