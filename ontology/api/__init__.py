from rest_framework import fields as drffields
from vstutils.utils import create_view
from vstutils.api.actions import EmptyAction
from vstutils.api.serializers import BaseSerializer
from ontology.models import models
from ontology.models.tasks import RouteTask
from ontology.constants import CargoType


AreaViewSet = create_view(
    models.Area,
    list_fields=(
        'name',
    ),
    detail_fields=(
        'name',
    ),
)


RouteViewSet = create_view(
    models.Route,
    list_fields=(
        'wherefrom',
        'whereto',
        'distance',
    ),
    detail_fields=(
        'wherefrom',
        'whereto',
        'distance',
    ),
)


TruckModelViewSet = create_view(
    models.TruckModel,
    list_fields=(
        'name',
        'load_capacity',
        'gas_tank_capacity',
        'fuel_consumption',
    ),
    detail_fields=(
        'name',
        'load_capacity',
        'gas_tank_capacity',
        'fuel_consumption',
    ),
)


TruckViewSet = create_view(
    models.Truck,
    list_fields=(
        'number',
        'model',
        'type',
        'location',
    ),
    detail_fields=(
        'number',
        'model',
        'type',
        'location',
    ),
    override_list_fields={
        'type': drffields.ChoiceField(choices=CargoType.to_choices()),
    },
    override_detail_fields={
        'type': drffields.ChoiceField(choices=CargoType.to_choices()),
    },
)


CargoViewSet = create_view(
    models.Cargo,
    list_fields=(
        'mass',
        'location',
        'destination',
        'type',
    ),
    detail_fields=(
        'mass',
        'location',
        'destination',
        'type',
    ),
    override_list_fields={
        'type': drffields.ChoiceField(choices=CargoType.to_choices()),
    },
    override_detail_fields={
        'type': drffields.ChoiceField(choices=CargoType.to_choices()),
    },
)


class ComputeRoutesSerializer(BaseSerializer):
    detail = drffields.CharField(read_only=True)


class ComputedRouteViewMixin:
    @EmptyAction(result_serializer_class=ComputeRoutesSerializer, detail=False)
    def compute_routes(self, request, *args, **kwargs):
        RouteTask.do()
        return {'detail': 'Routes being computed.'}


ComputedRouteViewSet = create_view(
    models.ComputedRoute,
    view_class=(ComputedRouteViewMixin, 'history'),
    list_fields=(
        'id',
        'truck',
        'cargo',
        'fuel',
    ),
    detail_fields=(
        'id',
        'truck',
        'cargo',
        'fuel',
        'path',
    ),
)
