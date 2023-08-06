import abc
from typing import List, Tuple, Dict, Callable

import stringcase
from django.db.models import QuerySet


from django_koldar_utils.django_toolbox import django_helpers
from django_koldar_utils.graphql_toolsbox.GraphQLHelper import GraphQLHelper

from django_graphene_crud_generator.IGraphQLEndpointComponent import IGraphQLEndpointComponent

from django_graphene_crud_generator.CrudBuildPhaseEnum import CrudBuildPhaseEnum
from django_graphene_crud_generator.crud_generator.contexts import CRUDBuildContext, CRUDRuntimeContext
from django_koldar_utils.graphql_toolsbox.graphql_types import TGrapheneArgument, TGrapheneType, TGrapheneMutation

from django_graphene_crud_generator.crud_generator.shared_components import AddCRUDRuntimeContextComponent
from django_graphene_crud_generator.generator.AbstractGraphQLMutationGenerator import AbstractGraphQLMutationGenerator
from django_graphene_crud_generator.generator.AbstractGraphQLQueryGenerator import AbstractGraphQLQueryGenerator


class ICrudGraphQLGenerator(abc.ABC):
    """
    Interface for creating graphql CRUD endpoints of a particular entity.
    These crud operations are production ready: this means that they are all authenticated by default.
    We rely on IGraphQLEndpointGenerator in order to generateg single operations
    """

    def _get_common_components(self, build_context: CRUDBuildContext) -> List[IGraphQLEndpointComponent]:
        """
        Components that are applied to all the graphql endpoint generators build with this instance.
        **Make sure to always call the super method!**

        :param build_context: information known at build time
        :return: components all the endpoint created with this class should have
        """
        return [
            AddCRUDRuntimeContextComponent()
        ]

    @abc.abstractmethod
    def _get_create_components(self, build_context: CRUDBuildContext) -> List[IGraphQLEndpointComponent]:
        """
        Components that are applied to all the create graphql endpoint generators build with this instance

        :param build_context: information known at build time
        :return: components to add. Added strictly after the common components
        """
        pass

    @abc.abstractmethod
    def _get_read_single_components(self, build_context: CRUDBuildContext) -> List[IGraphQLEndpointComponent]:
        """
        Components that are applied to all the read single graphql endpoint generators build with this instance

        :param build_context: information known at build time
        :return: components to add. Added strictly after the common components
        """
        pass

    @abc.abstractmethod
    def _get_read_all_components(self, build_context: CRUDBuildContext) -> List[IGraphQLEndpointComponent]:
        """
        Components that are applied to all the read all graphql endpoint generators build with this instance

        :param build_context: information known at build time
        :return: components to add. Added strictly after the common components
        """
        pass

    @abc.abstractmethod
    def _get_update_components(self, build_context: CRUDBuildContext) -> List[IGraphQLEndpointComponent]:
        """
        Components that are applied to all the update graphql endpoint generators build with this instance

        :param build_context: information known at build time
        :return: components to add. Added strictly after the common components
        """
        pass

    @abc.abstractmethod
    def _get_delete_components(self, build_context: CRUDBuildContext) -> List[IGraphQLEndpointComponent]:
        """
        Components that are applied to all the delete graphql endpoint generators build with this instance

        :param build_context: information known at build time
        :return: components to add. Added strictly after the common components
        """
        pass

    @abc.abstractmethod
    def _get_create_graphql_generators(self, crud_build_context: CRUDBuildContext) -> Dict[str, AbstractGraphQLMutationGenerator]:
        """
        A generator that creates several graphql endpoint generator, one per create endpoint

        :param crud_build_context: information know nat compile timer
        :return: a dictionary specifying multiple create endpoint. In this way you can add multiple create endpoint
            with a single implementation
        """
        pass

    @abc.abstractmethod
    def _get_read_single_graphql_generators(self, crud_build_context: CRUDBuildContext) -> Dict[str, AbstractGraphQLQueryGenerator]:
        """
        A generator that creates several graphql endpoint generator, one per read single endpoint

        :param crud_build_context: information know nat compile timer
        :return: a dictionary specifying multiple create endpoint. In this way you can add multiple read single endpoint
            with a single implementation
        """
        pass

    @abc.abstractmethod
    def _get_read_all_graphql_generators(self, crud_build_context: CRUDBuildContext) -> Dict[str, AbstractGraphQLQueryGenerator]:
        """
        A generator that creates several graphql endpoint generator, one per read all endpoint

        :param crud_build_context: information know nat compile timer
        :return: a dictionary specifying multiple create endpoint. In this way you can add multiple read all endpoint
            with a single implementation
        """
        pass

    @abc.abstractmethod
    def _get_update_graphql_generators(self, crud_build_context: CRUDBuildContext) -> Dict[str, AbstractGraphQLMutationGenerator]:
        """
        A generator that creates several graphql endpoint generator, one per update endpoint

        :param crud_build_context: information know nat compile timer
        :return: a dictionary specifying multiple create endpoint. In this way you can add multiple update endpoint
            with a single implementation
        """
        pass

    @abc.abstractmethod
    def _get_delete_graphql_generators(self, crud_build_context: CRUDBuildContext) -> Dict[str, AbstractGraphQLMutationGenerator]:
        """
        A generator that creates several graphql endpoint generator, one per delete endpoint

        :param crud_build_context: information know nat compile timer
        :return: a dictionary specifying multiple create endpoint. In this way you can add multiple delete endpoint
            with a single implementation
        """
        pass

    # def _activate_field_name(self, context: CRUDBuildContext) -> bool:
    #     """
    #     :return: Name of the field specifying whether or not a row is active
    #     """
    #     return "active"

    @abc.abstractmethod
    def _get_permissions_to_create(self, endpoint: str, context: CRUDBuildContext) -> List[str]:
        """
        Permissions that are required to a generic create endpoint
        :param endpoint: name of the endpoint whose permissions we need to return
        :param context: information know at buildtime
        :return: permissions for a specific graphql endpoint
        """
        pass

    @abc.abstractmethod
    def _get_permissions_to_read_single(self, endpoint: str, context: CRUDBuildContext) -> List[str]:
        """
        Permissions that are required to a generic read single endpoint
        :param endpoint: name of the endpoint whose permissions we need to return
        :param context: information know at buildtime
        :return: permissions for a specific graphql endpoint
        """
        pass

    @abc.abstractmethod
    def _get_permissions_to_update(self, endpoint: str, context: CRUDBuildContext) -> List[str]:
        """
        Permissions that are required to a generic update endpoint
        :param endpoint: name of the endpoint whose permissions we need to return
        :param context: information know at buildtime
        :return: permissions for a specific graphql endpoint
        """
        pass

    @abc.abstractmethod
    def _get_permissions_to_delete(self, endpoint: str, context: CRUDBuildContext) -> List[str]:
        """
        Permissions that are required to a generic create endpoint
        :param endpoint: name of the endpoint whose permissions we need to return
        :param context: information know at buildtime
        :return: permissions for a specific graphql endpoint
        """
        pass

    def generate(self,
                                 django_type: type, django_graphql_type: type, django_input_type: type,
                                 active_field_name: str = None,
                                 create_compare_fields: List[str] = None,
                                 generate_create: bool = True,
                                 generate_read_all: bool = True,
                                 generate_read_single: bool = True,
                                 generate_update: bool = True,
                                 generate_delete: bool = True,
                                 **kwargs
                                 ) -> Tuple[List[TGrapheneMutation], type, type, type, type]:
        """
        Generate a default create, update, delete operations. Delete actually just set the active field set to false.

        :param django_type: class deriving from models.Model
        :param django_graphql_type: class deriving from DjangoObjectType of graphene_toolbox package
        :param django_input_type: class deriving from DjangoInputObjectType from django_toolbox graphene_toolbox extras package
        :param active_field_name: name fo the active flag
        :param create_compare_fields: field used to check uniquness of the row when creating a new element. If missing, we will populate them with all the unique fields.
            Inactive rows are ignored
        :param generate_create: if true, we will generate the create mutation. Otherwise we will return None as the generated mutation class
        :param generate_read_all: if true, we will generate the read all mutation. Otherwise we will return None as the generated mutation class
        :param generate_read_single: if true, we will generate the read single mutatuion. Otherwise we will return None as the generated query class
        :param generate_update: if true, we will generate the update mutatuion. Otherwise we will return None as the generated query class
        :param generate_delete: if true, we will generate the delete mutatuion. Otherwise we will return None as the generated mutation class
        :param kwargs: set fo additional parameters you need to pass to the implementation of the graphql generator.
            Implementation dependent.
        :return: a tuple where each element is a class representing a mutation/query or None if the associated method "generate_" is set to False.
            - create mutation type
            - read all query type
            - update mutation type
            - delete mutation type
            - read single element query type
        """
        crud_build_context = CRUDBuildContext(django_type, django_graphql_type, django_input_type, kwargs)

        create = None
        read_single = None
        read_all = None
        update = None
        delete = None

        primary_key_name = django_helpers.get_name_of_primary_key(django_type)

        if generate_create:
            create = self._generate_mutation_create(
                crud_build_context=crud_build_context,
            )

        if generate_read_all:
            read_all = self._generate_mutation_read_all(
                build_context=crud_build_context
            )

        if generate_read_single:
            read_single = self._generate_mutation_read_single(
                build_context=crud_build_context
            )

        # if generate_update:
        #     update = cls.generate_mutation_update_primitive_data(
        #         django_type=django_type,
        #         django_graphql_type=django_graphql_type,
        #         django_input_type=django_input_type,
        #         permissions_required=permissions_required_update,
        #         mutation_class_name=class_names.get_update_name(django_type),
        #         output_name=class_names.get_update_return_value_name(django_type),
        #         token_name=token_name,
        #     )
        #
        # if generate_delete:
        #     delete = cls.generate_mutation_mark_inactive(
        #         django_type=django_type,
        #         django_graphql_type=django_graphql_type,
        #         django_input_type=django_input_type,
        #         active_flag_name=active_field_name,
        #         permissions_required=permissions_required_delete,
        #         mutation_class_name=class_names.get_delete_name(django_type),
        #         output_name=class_names.get_delete_return_value_name(django_type),
        #         token_name=token_name,
        #     )
        return create, read_all, update, delete, read_single

    # ######################################
    # APPLICABLE TO ANY ENDPOINT
    # ######################################

    # @abc.abstractmethod
    # def _get_parameters_to_add_to_all_graphql(self, context: CRUDBuildContext) -> Dict[str, TGrapheneArgument]:
    #     """
    #     Set of graphql parameters that will be added to any graphql endpoint. If the argument is already present,
    #     we will override the previous parameter
    #
    #     :param build_context: information known at build time
    #     """
    #     pass
    #
    # @abc.abstractmethod
    # def _patch_mutation_return_value(self, build_context: CRUDBuildContext, d: Dict[str, TGrapheneType]) -> Dict[str, TGrapheneType]:
    #     """
    #     A function that will revise any return value generated by the user. We may append additional return types,
    #     or rename them
    #
    #     :param build_context: information known at build time
    #     :param d: return value of a graphql query/mutation
    #     :return: formal return value of a grpahql query/mutation
    #     """
    #     pass

    # ######################################
    # READ SINGLE
    # ######################################

    # @abc.abstractmethod
    # def _read_single_query_class_name(self, build_context: CRUDBuildContext) -> str:
    #     """
    #     :param build_context: information known at build time
    #     :return: the name of thwe type representing this query
    #     """
    #     pass
    #     return f"Get{stringcase.pascalcase(build_context.django_type.__name__)}Item"
    #
    # @abc.abstractmethod
    # def _read_single_query_output_name(self, build_context: CRUDBuildContext) -> str:
    #     """
    #
    #     :param build_context: information known at build time
    #     :return: name of the field in the output of the read query
    #     """
    #
    #
    # @abc.abstractmethod
    # def _get_read_single_queryset_filter(self, queryset: QuerySet, runtime_context: CRUDRuntimeContext) -> QuerySet:
    #     """
    #     computes the result to show to the user when running the read single element query
    #
    #     :param queryset: the set of all the elements of type django_type
    #     :param runtime_context: information know when running the graphql endpoint
    #     :return: result to output to the query
    #     """
    #     pass
    #
    # def _read_single_query_description(self, build_context: CRUDBuildContext) -> str:
    #     """
    #
    #     :param build_context: information known at build time
    #     :return:
    #     """
    #     perms = self._get_permissions_to_read_single(build_context)
    #     return f"""Allows you to get a single element of {build_context.django_type.__name__} within the database.
    #     In order to run the query, you need the following permissions: {', '.join(perms)}
    #     """
    #
    # @abc.abstractmethod
    # def _read_single_query_arguments(self, build_context: CRUDBuildContext) -> Dict[str, TGrapheneArgument]:
    #     """
    #     :param build_context: information known at build time
    #     :return: arguments for the read single element query
    #     """
    #     pass
    #
    # def _read_single_body_decorator(self, build_context: CRUDBuildContext) -> Callable:
    #     """
    #     The decorator we use to decorate the actual read all query body. By default it is a no op operation
    #
    #     :param build_context: information known at build time
    #     """
    #
    #     def decorator(f):
    #         def wrapper(*args, **kwargs):
    #             return f(*args, **kwargs)
    #
    #         return wrapper
    #
    #     return decorator
    #
    # def _generate_mutation_read_single(self, build_context: CRUDBuildContext) -> type:
    #     arguments = self._read_single_query_arguments(build_context)
    #     arguments.update(self._get_parameters_to_add_to_all_graphql(build_context))
    #
    #     result, query_return_type = GraphQLHelper.generate_query_from_queryset_filter(
    #         django_type=build_context.django_type,
    #         query_class_name=self._read_single_query_class_name(build_context),
    #         description=self._read_single_query_description(build_context),
    #         output_name=self._read_single_query_output_name(build_context),
    #         return_multipler="optional",
    #         queryset_filter=lambda queryset, query_type, info, args, kwargs: self._get_read_single_queryset_filter(queryset, CRUDRuntimeContext(build_context, info, query_type, args, kwargs)),
    #         arguments=arguments,
    #         return_type=build_context.graphene_type,
    #         body_decorator=lambda django_type, query_class_name, arguments, return_type: self._read_single_body_decorator(build_context)
    #     )
    #
    #     build_context.read_single_parameters = arguments
    #     build_context.read_single_return_value = query_return_type
    #
    #     return result
    #
    # # ######################################
    # # READ ALL
    # # ######################################
    #
    # @abc.abstractmethod
    # def _read_all_query_class_name(self, build_context: CRUDBuildContext) -> str:
    #     """
    #
    #     :param build_context: information known at build time
    #     :return: the name of the type representing the query. It will autoamtically be converted into camel case by graphene
    #     """
    #     pass
    #
    # @abc.abstractmethod
    # def _get_read_all_queryset_filter(self, queryset: QuerySet, runtime_context: CRUDRuntimeContext) -> QuerySet:
    #     pass
    #     return queryset
    #
    # def _read_all_query_description(self, build_context: CRUDBuildContext) -> str:
    #     """
    #     :param build_context: information known at build time
    #     :return: the documentation attached to the read all query
    #     """
    #     perms = self._get_permissions_to_read_all(build_context)
    #     return f"""Allows you to get all the {build_context.django_type.__name__} within the database. In order to
    #     execute the query, you need to following permissions: {', '.join(perms)}
    #     """
    #
    # @abc.abstractmethod
    # def _read_all_query_output_name(self, build_context: CRUDBuildContext) -> str:
    #     """
    #
    #     :param build_context: information known at build time
    #     :return: name of the field in the output of the read query
    #     """
    #
    # @abc.abstractmethod
    # def _read_all_query_arguments(self, build_context: CRUDBuildContext) -> Dict[str, TGrapheneArgument]:
    #     """
    #     :param build_context: information known at build time
    #     :return: arguments of the query read all elements
    #     """
    #     pass
    #
    # def _read_all_body_decorator(self, build_context: CRUDBuildContext) -> Callable:
    #     """
    #     The decorator we use to decorate the actual read all query body
    #
    #     :param build_context: information known at build time
    #     """
    #     def decorator(f):
    #         def wrapper(*args, **kwargs):
    #             return f(*args, **kwargs)
    #         return wrapper
    #     return decorator
    #
    # @abc.abstractmethod
    # def _get_permissions_to_read_all(self, context: CRUDBuildContext) -> List[str]:
    #     """
    #     :return: list of permissions required by the client in order to run the read all query
    #     """
    #     pass
    #
    # def _generate_mutation_read_all(self, build_context: CRUDBuildContext) -> type:
    #     arguments = self._read_all_query_arguments(build_context)
    #     arguments.update(self._get_parameters_to_add_to_all_graphql(build_context))
    #
    #     result, query_return_type = GraphQLHelper.generate_query_from_queryset_filter(
    #         django_type=build_context.django_type,
    #         query_class_name=self._read_all_query_class_name(build_context),
    #         description=self._read_all_query_description(build_context),
    #         output_name=self._read_all_query_output_name(build_context),
    #         return_multipler="multi",
    #         queryset_filter=lambda queryset, query_type, info, args, kwargs: self._get_read_all_queryset_filter(queryset, CRUDRuntimeContext(build_context, info, query_type, args, kwargs)),
    #         arguments=arguments,
    #         return_type=build_context.graphene_type,
    #         body_decorator=lambda django_type, query_class_name, arguments, return_type: self._read_all_body_decorator(build_context)
    #     )
    #
    #     build_context.read_all_parameters = arguments
    #     build_context.read_all_return_value = query_return_type
    #
    #     return result

    # ######################################
    # CREATE
    # ######################################

    # def _create_mutation_description(self, context: CRUDBuildContext) -> str:
    #     """
    #     the description of the create mutation
    #     """
    #     perms = self._get_permissions_to_create(context)
    #
    #     description = f"""Allows you to create a new instance of {context.django_type.__name__}.
    #         If the object is already present we do nothing.
    #     """
    #     if len(perms) > 0:
    #         description += f"""Note that you need to authenticate your user in order to use this mutation.
    #             The permission your user is required to have are: {', '.join(perms)}.
    #         """
    #     return description
    #
    # @abc.abstractmethod
    # def _create_mutation_class_name(self, context: CRUDBuildContext) -> str:
    #     """
    #     mutation class name
    #     """
    #     pass
    #
    # @abc.abstractmethod
    # def _create_mutation_parameters(self, context: CRUDBuildContext) -> Dict[str, TGrapheneArgument]:
    #     """
    #     create mutation graphql parameters
    #     """
    #     pass
    #
    # @abc.abstractmethod
    # def _create_mutation_return_value(self, context: CRUDBuildContext) -> Dict[str, TGrapheneReturnType]:
    #     """
    #     create mutation graphql return values
    #     """
    #     pass
    #
    # @abc.abstractmethod
    # def _check_if_object_exists(self, django_type: TDjangoModelType, runtime_context: CRUDRuntimeContext) -> Tuple[bool, Optional[models.Model]]:
    #     """
    #     Check if a particular element already exists in the database
    #
    #     :param django_type: type of the model to fetch
    #     :param info: graphql info value
    #     :param args: graphql args
    #     :param kwargs: graphql kwargs
    #     :return: true if the object already exists in the database, false otherwise. The second item of the tuple
    #         represents the element already stored in the database. Notice that this value is optional for the
    #         implementation to implement. In other words if can be None even if the object is already present in the
    #         database
    #     """
    #     pass
    #
    # @abc.abstractmethod
    # def _add_new_object_in_database(self, django_type: TDjangoModelType, runtime_context: CRUDRuntimeContext) -> any:
    #     """
    #     Adds a new object in the database. You are ensured that the object does not yet exist in the database
    #
    #     :param django_type: type of the model to fetch
    #     :param runtime_context: data availalbe to us while running the query
    #     :return: anything you want. It should repersents the added row though
    #     """
    #     pass
    #
    # @abc.abstractmethod
    # def _check_new_object_return_value(self, result: any, django_type: TDjangoModelType, runtime_context: CRUDRuntimeContext):
    #     """
    #     Check if the output of _add_new_object_in_database represents a successful operation or not
    #
    #     :param result: output of _add_new_object_in_database
    #     :param django_type: type of the model to fetch
    #     :param runtime_context: data availalbe to us while running the query
    #     """
    #     pass
    #
    # @abc.abstractmethod
    # def _create_generate_mutation_instance_row_already_exists(self, mutation_class: type, item_in_db: models.Model, runtime_context: CRUDRuntimeContext) -> any:
    #     """
    #     code used to create the instance of the create mutation class when the element to add is already
    #     present in the database
    #
    #     :param mutation_class: type of the create mutation
    #     :param item_in_db: the object that is already present in the database. By contract it can be None even if
    #         the object is stored in the database. Do not assume anything if this value
    #         is None!
    #     :return: instance of mutation_class
    #     """
    #     pass
    #
    # @abc.abstractmethod
    # def _create_generate_mutation_instance_row_added(self, mutation_class: type, result: any, runtime_context: CRUDRuntimeContext) -> any:
    #     """
    #     code used to create the instance of the create mutation class when the element to add has
    #     been successfully added
    #
    #     :param mutation_class: type of the create mutation
    #     :return: instance of mutation_class
    #     """
    #     pass
    #
    # def _create_mutation_decorate_body(self, build_context: CRUDBuildContext):
    #     """
    #     generate a decorator that will decorate the actual mutation body. graphql body function
    #     follows this signature:
    #
    #     .. code-block::
    #
    #         def body(mutation_class, info, *args, **kwargs) -> any:
    #
    #
    #     By default we will generate a noop decorator
    #     :param build_context: data available at buildtime
    #     """
    #     def result(f):
    #         def wrapper(*args, **kwargs):
    #             return f(*args, **kwargs)
    #         return wrapper
    #     return result

    def _generate_mutation_create(self, crud_build_context: CRUDBuildContext) -> List[TGrapheneMutation]:
        """
        Create a mutation that adds a new element in the database.
        We will generate a mutation that accepts a single input parameter. It checks if the input is not already present in the database and if not, it adds it.
        The returns the data added in the database.
        This method can already integrate graphene_jwt to authenticate and authorize users

        :param crud_build_context: object containing data availalbe while genrating the graphql mutations and queries
        :return: class rerpesenting the mutation
        """

        result = []

        crud_build_context.build_phase = CrudBuildPhaseEnum.CREATE
        kwargs = crud_build_context.params
        kwargs["crud_build_context"] = crud_build_context

        for name, generator in self._get_create_graphql_generators(crud_build_context).items():
            generator.register_component(*self._get_common_components(crud_build_context))
            generator.register_component(*self._get_create_components(crud_build_context))
            result.append(generator.generate(
                permissions=self._get_permissions_to_create(name, crud_build_context), **kwargs
            ))

        return result

        # mutation_class_name = self._create_mutation_class_name(build_context)
        # description = self._create_mutation_description(build_context)
        # mutation_arguments = self._create_mutation_parameters(build_context)
        # mutation_arguments.update(self._get_parameters_to_add_to_all_graphql(build_context))
        # mutation_return_value = self._create_mutation_return_value(build_context)
        # mutation_return_value = self._patch_mutation_return_value(build_context, mutation_return_value)
        # build_context.create_return_value = mutation_return_value
        # build_context.create_parameters = mutation_arguments
        #
        # def body(mutation_class, info, *args, **kwargs) -> any:
        #     runtime_context = CRUDRuntimeContext(build_context, info, mutation_class, *args, **kwargs)
        #     exists, item_in_db = self._check_if_object_exists(build_context.django_type, runtime_context)
        #     if exists:
        #         return self._create_generate_mutation_instance_row_already_exists(mutation_class, item_in_db, runtime_context)
        #     # add the instance
        #     create_result = self._add_new_object_in_database(build_context.django_type, runtime_context)
        #     result = self._create_generate_mutation_instance_row_added(mutation_class, create_result, runtime_context)
        #     return result
        #
        # return GraphQLHelper.create_mutation(
        #     mutation_class_name=mutation_class_name,
        #     description=description,
        #     arguments=mutation_arguments,
        #     return_type=mutation_return_value,
        #     body=self._create_mutation_decorate_body(build_context)(body)
        # )

