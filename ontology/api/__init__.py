from django.db import transaction
from rest_framework import fields as drffields
from vstutils.utils import create_view
from vstutils.api.actions import EmptyAction
from vstutils.api.serializers import BaseSerializer
from vstutils.api import fields as vstfields
from ontology.models import models
from ontology.models.tasks import RouteTask
from ontology.models.algorithms import compute_routes
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

        # with transaction.atomic():
        #     routes = compute_routes()
        #     models.ComputedRoute.objects.all().delete()
        #     for route in routes:
        #         route.save()

        return {'detail': 'Routes being computed.'}


ComputedRouteViewSet = create_view(
    models.ComputedRoute,
    view_class=(ComputedRouteViewMixin, 'history'),
    list_fields=(
        'id',
        'truck',
        'cargo',
        'distance',
    ),
    detail_fields=(
        'id',
        'truck',
        'cargo',
        'distance',
        'fuel',
        'path',
    ),
    override_list_fields={
        'truck': vstfields.FkModelField(
            select=models.Truck,
            autocomplete_represent='number',
        ),
        'cargo': vstfields.FkModelField(
            select=models.Cargo,
            autocomplete_represent='id',
        ),
    },
    override_detail_fields={
        'truck': vstfields.FkModelField(
            select=models.Truck,
            autocomplete_represent='number',
        ),
        'cargo': vstfields.FkModelField(
            select=models.Cargo,
            autocomplete_represent='id',
        ),
        'path': drffields.ListField(child=vstfields.FkModelField(select=models.Area)),
    },
)
