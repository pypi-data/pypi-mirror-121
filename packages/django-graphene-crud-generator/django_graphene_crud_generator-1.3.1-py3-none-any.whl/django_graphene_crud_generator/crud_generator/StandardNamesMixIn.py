# from typing import Dict
#
# import stringcase
# from django_koldar_utils.graphql.graphql_types import TGrapheneType
#
# from django_graphene_crud_generator.crud_generator.contexts import CRUDBuildContext
#
#
#
#
# class StandardNamesMixIn:
#     """
#     A simple implementation to generate the names of all the relevant graphql names and return values
#     """
#
#
#     def _read_single_query_name(self, build_context: CRUDBuildContext) -> str:
#         return f"readSingle{stringcase.pascalcase(build_context.django_type.__name__)}Item"
#
#     def _read_all_query_name(self, build_context: CRUDBuildContext) -> str:
#         return f"readAll{stringcase.pascalcase(build_context.django_type.__name__)}Items"
#
#     def _create_mutation_class_name(self, build_context: CRUDBuildContext) -> str:
#         return f"create{stringcase.pascalcase(build_context.django_type.__name__)}Item"
#
#     def _patch_mutation_return_value(self, build_context: CRUDBuildContext, d: Dict[str, TGrapheneType]) -> Dict[str, TGrapheneType]:
#         return d
#
#     def _read_single_query_output_name(self, build_context: CRUDBuildContext) -> str:
#         return f"result"
#
#     def _read_all_query_output_name(self, build_context: CRUDBuildContext) -> str:
#         return f"result"
