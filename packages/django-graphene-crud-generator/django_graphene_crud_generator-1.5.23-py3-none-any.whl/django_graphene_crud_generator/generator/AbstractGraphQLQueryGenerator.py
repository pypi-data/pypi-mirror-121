import abc

import graphene
from django_koldar_utils.graphql_toolsbox import graphql_decorators

from django_graphene_crud_generator.generator.IGraphQLEndpointGenerator import IGraphQLEndpointGenerator
from django_graphene_crud_generator.generator.contexts import GraphQLBuildtimeContext


class AbstractGraphQLQueryGenerator(IGraphQLEndpointGenerator, abc.ABC):
    """
    Generate a query via graphene and automatically registers it with graphql_subquery decorator
    """

    @abc.abstractmethod
    def _get_return_value_name(self, build_context: GraphQLBuildtimeContext) -> str:
        """
        generate the field name in the output that contains the output of the query
        :param build_context:context known at build time
        :return: name fo the field
        """
        pass

    # @abc.abstractmethod
    # def _get_return_value_temp_type_name(self, builld_context: GraphQLBuildtimeContext) -> str:
    #     pass

    def _compute_graphene_class(self, build_context: GraphQLBuildtimeContext) -> type:
        if isinstance(build_context.action_return_type, graphene.Field):
            # needed otherwise graphene_toolbox.schema will raise an exception
            build_context.action_return_type = build_context.action_return_type.type

        output_name = self._get_return_value_name(build_context)

        assert output_name is not None, f"output name of graphene class \"{build_context.action_class_name}\" is none!"

        properties = dict()
        properties["__doc__"] = build_context.action_description,
        properties[f"resolve_{output_name}"] = build_context.action_body
        properties[output_name] = graphene.Field(build_context.action_return_type, args=build_context.action_arguments)

        query_class = type(
            build_context.action_class_name,
            (graphene.ObjectType, ),
            properties
        )
        # Apply decorator to auto detect queries
        decorated_query_class = graphql_decorators.graphql_subquery(query_class)

        return decorated_query_class