import functools

import stringcase
from django_koldar_utils.graphql_toolsbox.graphql_types import TGrapheneWholeQueryReturnType

from django_graphene_crud_generator.IGraphQLEndpointComponent import IGraphQLEndpointComponent
from django_graphene_crud_generator.CrudBuildPhaseEnum import CrudBuildPhaseEnum
from django_graphene_crud_generator.crud_generator.AbstractGraphQLCrudComponent import AbstractGraphQLCrudComponent
from django_graphene_crud_generator.crud_generator.contexts import CRUDBuildContext, CRUDRuntimeContext
from django_graphene_crud_generator.generator.contexts import GraphQLBuildtimeContext, GraphQLRuntimeContext
from django_graphene_crud_generator.types import GrapheneGeneratorBodyFunction


from typing import Dict, Callable, List, Tuple

from django_koldar_utils.django_toolbox import auth_decorators
from django_koldar_utils.graphql_toolsbox.GraphQLHelper import GraphQLHelper
from django_koldar_utils.graphql_toolsbox.graphql_types import TGrapheneArgument

from django_graphene_crud_generator.crud_generator.contexts import CRUDBuildContext


class AddCRUDRuntimeContextComponent(AbstractGraphQLCrudComponent):
    """
    Add to the runtime_context
    """

    def _graphql_body_function_decorator(self, runtime_context: GraphQLRuntimeContext):
        def decorator(generator_body):
            @functools.wraps(generator_body)
            def wrapper(*args, **kwargs):
                nonlocal self
                runtime_context.params["crud_runtime_context"] = CRUDRuntimeContext(
                    c=self.crud_build_context(runtime_context.build_context),
                    info=runtime_context.info,
                    graphql_class=runtime_context.root,
                    *runtime_context.args, **runtime_context.kwargs
                )
                return generator_body(*args, **kwargs)
            return wrapper
        return decorator


class FederatedNamesCrudComponent(AbstractGraphQLCrudComponent):
    """
    If you are developing a federation, the names within the federation needs to be unique.
    This namer enforces it. We assume the user has passed a parameters called "subgraph_name"
    during the init of the crud graphql generator
    """

    def subgraph_name(self, crud_build_context: CRUDBuildContext) -> str:
        return crud_build_context.params["subgraph_name"]

    def _generate_action_class_name(self, build_context: GraphQLBuildtimeContext) -> str:
        crud_build_context = self.crud_build_context(build_context)
        django_type = crud_build_context.django_type
        if crud_build_context.build_phase == CrudBuildPhaseEnum.CREATE:
            return f"{stringcase.camelcase(self.subgraph_name(crud_build_context))}Create{stringcase.pascalcase(django_type.__name__)}Item"
        elif crud_build_context.build_phase == CrudBuildPhaseEnum.READ_SINGLE:
            return f"{stringcase.camelcase(self.subgraph_name(crud_build_context))}ReadSingle{stringcase.pascalcase(django_type.__name__)}Item"
        elif crud_build_context.build_phase == CrudBuildPhaseEnum.READ_ALL:
            return f"{stringcase.camelcase(self.subgraph_name(crud_build_context))}ReadAll{stringcase.pascalcase(django_type.__name__)}Items"
        elif crud_build_context.build_phase == CrudBuildPhaseEnum.UPDATE:
            return f"{stringcase.camelcase(self.subgraph_name(crud_build_context))}Update{stringcase.pascalcase(django_type.__name__)}Items"
        elif crud_build_context.build_phase == CrudBuildPhaseEnum.DELETE:
            return f"{stringcase.camelcase(self.subgraph_name(crud_build_context))}Delete{stringcase.pascalcase(django_type.__name__)}Items"
        else:
            raise ValueError(f"invalid build phase {crud_build_context.build_phase}")

    def _generate_action_return_type(self, build_context: GraphQLBuildtimeContext) -> Tuple[str, TGrapheneWholeQueryReturnType]:
        crud_build_context = self.crud_build_context(build_context)
        django_type = crud_build_context.django_type
        if crud_build_context.build_phase == CrudBuildPhaseEnum.CREATE:
            result = dict()
            for k, v in list(build_context.action_return_type.items()):
                result[f"{stringcase.camelcase(self.subgraph_name(crud_build_context))}{stringcase.pascalcase(k)}"] = v
        elif crud_build_context.build_phase == CrudBuildPhaseEnum.READ_SINGLE:
            result = dict()
            for k, v in build_context.action_return_type.items():
                result[f"{stringcase.camelcase(self.subgraph_name(crud_build_context))}{stringcase.pascalcase(k)}"] = v
        elif crud_build_context.build_phase == CrudBuildPhaseEnum.READ_ALL:
            result = dict()
            for k, v in build_context.action_return_type.items():
                result[f"{stringcase.camelcase(self.subgraph_name(crud_build_context))}{stringcase.pascalcase(k)}"] = v
        elif crud_build_context.build_phase == CrudBuildPhaseEnum.UPDATE:
            result = dict()
            for k, v in build_context.action_return_type.items():
                result[f"{stringcase.camelcase(self.subgraph_name(crud_build_context))}{stringcase.pascalcase(k)}"] = v
        elif crud_build_context.build_phase == CrudBuildPhaseEnum.DELETE:
            result = dict()
            for k, v in build_context.action_return_type.items():
                result[f"{stringcase.camelcase(self.subgraph_name(crud_build_context))}{stringcase.pascalcase(k)}"] = v
        else:
            raise ValueError(f"invalid build phase {crud_build_context.build_phase}")

        return "set", result


class StandardNamesComponent(AbstractGraphQLCrudComponent):
    """
    A simple implementation to generate the names of all the relevant graphql names and return values
    """

    def _generate_action_class_name(self, build_context: GraphQLBuildtimeContext) -> str:
        crud_build_context = self.crud_build_context(build_context)
        if crud_build_context.build_phase == CrudBuildPhaseEnum.CREATE:
            return f"create{stringcase.pascalcase(crud_build_context.django_type.__name__)}Item"
        elif crud_build_context.build_phase == CrudBuildPhaseEnum.READ_SINGLE:
            return f"readSingle{stringcase.pascalcase(crud_build_context.django_type.__name__)}Item"
        elif crud_build_context.build_phase == CrudBuildPhaseEnum.READ_ALL:
            return f"readAll{stringcase.pascalcase(crud_build_context.django_type.__name__)}Items"
        elif crud_build_context.build_phase == CrudBuildPhaseEnum.UPDATE:
            return f"update{stringcase.pascalcase(crud_build_context.django_type.__name__)}Item"
        elif crud_build_context.build_phase == CrudBuildPhaseEnum.DELETE:
            return f"delete{stringcase.pascalcase(crud_build_context.django_type.__name__)}Item"
        else:
            raise ValueError(f"invalid build phase {crud_build_context.build_phase}")

    def _generate_action_return_type(self, build_context: GraphQLBuildtimeContext) -> TGrapheneWholeQueryReturnType:
        return "update", dict()
