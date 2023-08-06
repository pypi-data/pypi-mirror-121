from typing import Callable, List, Dict

from django_graphene_crud_generator.generator.contexts import GraphQLRuntimeContext

GrapheneGeneratorBodyFunction = Callable[[GraphQLRuntimeContext, List[any], Dict[str, any]], any]
"""
type fo graphene body function. Specific of IgraphQLEndpointGenerator
"""

GrapheneBodyFunction = Callable[[any, any, List[any], Dict[str, any]], any]
"""
type of grapghene boduy function. Compliant with graphene mutate/resolve methods
"""