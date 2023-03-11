from django.db.utils import IntegrityError
from vstutils.tests import BaseTestCase
from ontology.models import models


class ConstraintsTestCase(BaseTestCase):
    def setUp(self):
        self.area1 = models.Area.objects.create(name='area1')
        self.area2 = models.Area.objects.create(name='area2')

    def test_route_wherefrom_whereto_different(self):
        with self.assertRaises(IntegrityError):
            models.Route.objects.create(
                wherefrom=self.area1,
                whereto=self.area1,
                distance=1,
            )

    def test_cargo_location_destination_different(self):
        with self.assertRaises(IntegrityError):
            models.Cargo.objects.create(
                location=self.area1,
                destination=self.area1,
                type='type',
                mass=1,
            )

    def test_route_distance_gt0(self):
        with self.assertRaises(IntegrityError):
            models.Route.objects.create(
                wherefrom=self.area1,
                whereto=self.area2,
                distance=-1,
            )

    def test_truck_model_load_capacity_gt0(self):
        with self.assertRaises(IntegrityError):
            models.TruckModel.objects.create(
                name='truck_model1',
                load_capacity=-1,
                gas_tank_capacity=1,
                fuel_consumption=1,
            )

    def test_truck_model_gas_tank_capacity_gt0(self):
        with self.assertRaises(IntegrityError):
            models.TruckModel.objects.create(
                name='truck_model2',
                load_capacity=1,
                gas_tank_capacity=-1,
                fuel_consumption=1,
            )

    def test_truck_model_fuel_consumption_gt0(self):
        with self.assertRaises(IntegrityError):
            models.TruckModel.objects.create(
                name='truck_model3',
                load_capacity=1,
                gas_tank_capacity=1,
                fuel_consumption=-1,
            )

    def test_cargo_mass_gt0(self):
        with self.assertRaises(IntegrityError):
            models.Cargo.objects.create(
                mass=-1,
                type='type',
                location=self.area1,
                destination=self.area2,
            )

    def test_truck_model_gas_tank_capacity_gt_fuel_consumption(self):
        with self.assertRaises(IntegrityError):
            models.TruckModel.objects.create(
                name='truck_model1',
                load_capacity=1,
                gas_tank_capacity=1,
                fuel_consumption=999,
            )

    def test_unique_wherefrom_whereto(self):
        with self.assertRaises(IntegrityError):
            models.Route.objects.create(
                wherefrom=self.area1,
                whereto=self.area2,
                distance=1,
            )
            models.Route.objects.create(
                wherefrom=self.area1,
                whereto=self.area2,
                distance=1,
            )

    def test_unique_reversed_wherefrom_whereto(self):
        with self.assertRaises(IntegrityError):
            models.Route.objects.create(
                wherefrom=self.area1,
                whereto=self.area2,
                distance=1,
            )
            models.Route.objects.create(
                wherefrom=self.area2,
                whereto=self.area1,
                distance=1,
            )
