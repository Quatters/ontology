from django.db.models import (
    CASCADE,
    CheckConstraint,
    UniqueConstraint,
    CharField,
    FloatField,
    JSONField,
    F,
    Q,
)
from vstutils.models import BModel
from vstutils.models.fields import FkModelField
from vstutils.utils import lazy_translate as __


class Area(BModel):
    name = CharField(max_length=64, db_index=True)

    class Meta:
        ordering = ['name']


class Route(BModel):
    wherefrom = FkModelField(Area, on_delete=CASCADE, related_name='wherefrom_routes')
    whereto = FkModelField(Area, on_delete=CASCADE, related_name='whereto_routes')
    distance = FloatField()

    class Meta:
        constraints = [
            CheckConstraint(
                check=~Q(wherefrom=F('whereto')),
                name='different_wherefrom_whereto',
            ),
            CheckConstraint(
                check=Q(distance__gt=0),
                name='distance_gt0',
            ),
            UniqueConstraint(
                fields=['wherefrom', 'whereto'],
                name='unique_wherefrom_whereto',
            ),
        ]


class TruckModel(BModel):
    name = CharField(max_length=64, db_index=True)
    load_capacity = FloatField()
    gas_tank_capacity = FloatField()
    fuel_consumption = FloatField()

    class Meta:
        ordering = ['name'],
        constraints = [
            CheckConstraint(
                check=Q(load_capacity__gt=0),
                name='load_capacity_gt0',
            ),
            CheckConstraint(
                check=Q(gas_tank_capacity__gt=0),
                name='gas_tank_capacity_gt0',
            ),
            CheckConstraint(
                check=Q(fuel_consumption__gt=0),
                name='fuel_consumption_gt0',
            ),
            CheckConstraint(
                check=Q(gas_tank_capacity__gt=F('fuel_consumption')),
                name='gas_tank_capacity_gt_fuel_consumption',
            ),
        ]


class Truck(BModel):
    number = CharField(max_length=16, db_index=True, unique=True)
    model = FkModelField(TruckModel, on_delete=CASCADE)
    type = CharField(max_length=24, db_index=True)
    location = FkModelField(Area, on_delete=CASCADE)

    class Meta:
        default_related_name = 'trucks'
        ordering = ['number']


class Cargo(BModel):
    mass = FloatField()
    location = FkModelField(Area, on_delete=CASCADE, related_name='cargos_location')
    destination = FkModelField(Area, on_delete=CASCADE, related_name='cargos_destination')
    type = CharField(max_length=24, db_index=True)

    class Meta:
        constraints = [
            CheckConstraint(
                check=~Q(location=F('destination')),
                name='different_location_destination',
            ),
            CheckConstraint(
                check=Q(mass__gt=0),
                name='mass_gt0',
            ),
        ]


class ComputedRoute(BModel):
    truck = FkModelField(Truck, on_delete=CASCADE)
    cargo = FkModelField(Cargo, on_delete=CASCADE)
    fuel = FloatField()
    path = JSONField(default=list)

    class Meta:
        default_related_name = 'computed_routes'
