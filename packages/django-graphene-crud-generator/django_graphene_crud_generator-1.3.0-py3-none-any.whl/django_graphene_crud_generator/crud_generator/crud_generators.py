import abc
from typing import List, Dict, Callable

from django.db.models import QuerySet
from django_koldar_utils.django_toolbox import auth_decorators
from django_koldar_utils.graphql_toolsbox.graphql_types import TGrapheneReturnType, TGrapheneArgument

from django_graphene_crud_generator.ICrudGraphQLGenerator import ICrudGraphQLGenerator
from django_graphene_crud_generator.IGraphQLEndpointComponent import IGraphQLEndpointComponent
from django_graphene_crud_generator.crud_generator.contexts import CRUDBuildContext
from django_graphene_crud_generator.crud_generator.mixins import CanXPermissionsGraphQLCrudGeneratorMixIn
from django_graphene_crud_generator.generator.AbstractGraphQLMutationGenerator import AbstractGraphQLMutationGenerator
from django_graphene_crud_generator.generator.AbstractGraphQLQueryGenerator import AbstractGraphQLQueryGenerator
from django_graphene_crud_generator.generator.PermissionsComponent import PermissionComponent
from django_graphene_crud_generator.generator.TokenBasedAuthenticationComponent import TokenBasedAuthenticationComponent

from django_graphene_crud_generator.crud_generator import shared_components, create_components


class StandardFederatedCrudGenerator(CanXPermissionsGraphQLCrudGeneratorMixIn, ICrudGraphQLGenerator):
    """
    Use this class when you want to generate crud operation tthat fully support graphql federations.
    """

    def __init__(self):
        super().__init__()

    def _get_create_graphql_generators(self, crud_build_context: CRUDBuildContext) -> Dict[str, AbstractGraphQLMutationGenerator]:
        return dict(
            default=create_components.StandardCrudCreateMutation()
        )

    def _get_read_single_graphql_generators(self, crud_build_context: CRUDBuildContext) -> Dict[
        str, AbstractGraphQLQueryGenerator]:
        return dict()

    def _get_read_all_graphql_generators(self, crud_build_context: CRUDBuildContext) -> Dict[
        str, AbstractGraphQLQueryGenerator]:
        return dict()

    def _get_update_graphql_generators(self, crud_build_context: CRUDBuildContext) -> AbstractGraphQLMutationGenerator:
        return dict()

    def _get_delete_graphql_generators(self, crud_build_context: CRUDBuildContext) -> AbstractGraphQLMutationGenerator:
        return dict()

    def _get_common_components(self, build_context: CRUDBuildContext) -> List[IGraphQLEndpointComponent]:
        result = super()._get_common_components(build_context)
        result.extend([
            TokenBasedAuthenticationComponent(),
            shared_components.FederatedNamesCrudComponent(),
            PermissionComponent(),
        ])
        return result

    def _get_create_components(self, build_context: CRUDBuildContext) -> List[IGraphQLEndpointComponent]:
        return [
            create_components.CreateMutationReturnAddedValueComponent(),
            create_components.CreateMutationByInputtingSingleInput(),
        ]

    def _get_read_single_components(self, build_context: CRUDBuildContext) -> List[IGraphQLEndpointComponent]:
        return []

    def _get_read_all_components(self, build_context: CRUDBuildContext) -> List[IGraphQLEndpointComponent]:
        return []

    def _get_update_components(self, build_context: CRUDBuildContext) -> List[IGraphQLEndpointComponent]:
        return []

    def _get_delete_components(self, build_context: CRUDBuildContext) -> List[IGraphQLEndpointComponent]:
        return []


class StandardSimpleCrudGenerator(StandardFederatedCrudGenerator):
    """
    Use this class when you want to generate crud operation whose names are not cluttered with federation namespaces.
    However the schema generated will likely not be federation compatible.
    """

    def _get_common_components(self, build_context: CRUDBuildContext) -> List[IGraphQLEndpointComponent]:
        result = super()._get_common_components(build_context)
        result.extend([
            TokenBasedAuthenticationComponent(),
            shared_components.StandardNamesComponent(),
            PermissionComponent(),
        ])
        return result
