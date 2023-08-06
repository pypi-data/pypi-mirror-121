import abc
from typing import Dict, List, Callable

from django_koldar_utils.graphql_toolsbox.graphql_types import TGrapheneArgument, TGrapheneWholeQueryReturnType

from django_graphene_crud_generator.generator.contexts import GraphQLBuildtimeContext, GraphQLRuntimeContext
from django_graphene_crud_generator.types import GrapheneGeneratorBodyFunction, GrapheneBodyFunction


class IGraphQLEndpointComponent(abc.ABC):

    def _generate_action_arguments(self, build_context: GraphQLBuildtimeContext) -> Dict[str, TGrapheneArgument]:
        """
        Use "dict()" if you don't want to add anything to the arguments
        :return: list of parameters the class to generate will have. These are the graphql parameter
        """
        return dict()

    def _generate_action_description(self, build_context: GraphQLBuildtimeContext) -> List[str]:
        """
        Use "[]" if you don't want to add anything to the description

        :return: __doc__ of the class representing this action. Eac element in the list repersents a documentation
        paragraph. Paragraphs are then join together with "\n"
        """
        return []

    def _generate_action_return_type(self, build_context: GraphQLBuildtimeContext) -> TGrapheneWholeQueryReturnType:
        """
        Use "dict()" if you don't want to alter the return type in any way
        :return: list of parameters the class to generate will have. These are the graphql parameter
        """
        return dict()

    def _generate_action_class_name(self, build_context: GraphQLBuildtimeContext) -> str:
        """
        Use "build_context.action_class_name" if you don't want to alter the class name
        :return: name of the class representing this action
        """
        return build_context.action_class_name

    def _graphql_body_function_decorator_native(self, body_function: GrapheneBodyFunction, runtime_context: GraphQLRuntimeContext):
        """
        A function that agument the standard body function of the endpoint.
        Use "body_function" if you don't want to alter the function in any way

        :param body_function: body function to call. parameters are:
         - grpahql class
         - graphql info
         - graphql args
         - graphql kwargs
         - the grpahql endpioint result
        :return:
        """
        return body_function

    def _graphql_body_function_decorator(self, body_function: GrapheneGeneratorBodyFunction, runtime_context: GraphQLRuntimeContext):
        """
        A function that agument the standard body function of the endpoint.
        Use "body_function" if you don't want to alter the function in any way

        :param body_function: body function to call. parameters are:
         - grpahql runtime
         - graphql args
         - graphql kwargs
         - the grpahql endpioint result
        :return:
        """
        return body_function