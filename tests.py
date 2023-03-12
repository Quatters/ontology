from django.db.utils import IntegrityError
from vstutils.tests import BaseTestCase
from ontology.models import models
from ontology.constants import CargoType


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


class RouteComputingTestCase(BaseTestCase):
    def setUp(self):
        super().setUp()
        self.truck_model1 = models.TruckModel.objects.create(
            name='truck_model1',
            load_capacity=100,
            gas_tank_capacity=100,
            fuel_consumption=10,
        )

    def make_calculations(self):
        self.bulk_transactional([
            {'method': 'post', 'path': ['computed_routes', 'compute_routes']},
        ])

    def get_calculated_routes_list(self):
        results = self.bulk_transactional([
            {'method': 'get', 'path': 'computed_routes'},
        ])
        return results[0]['data']['results'], results[0]['data']['count']

    def get_calculated_route(self, route_id):
        results = self.bulk_transactional([
            {'method': 'get', 'path': ['computed_routes', route_id]},
        ])
        return results[0]['data']

    def test_simple(self):
        area1 = models.Area.objects.create(name='area1')
        area2 = models.Area.objects.create(name='area2')

        models.Route.objects.create(
            wherefrom=area1,
            whereto=area2,
            distance=10,
        )

        truck1 = models.Truck.objects.create(
            model=self.truck_model1,
            number='truck1',
            type=CargoType.Bulk,
            location=area1,
        )
        cargo1 = models.Cargo.objects.create(
            type=CargoType.Bulk,
            location=area1,
            destination=area2,
            mass=100,
        )

        # create cargo which cannot be delivered
        models.Cargo.objects.create(
            type=CargoType.Filler,
            location=area2,
            destination=area1,
            mass=90,
        )
        models.Cargo.objects.create(
            type=CargoType.Bulk,
            location=area2,
            destination=area1,
            mass=1000,
        )
        # create not suitable trucks
        models.Truck.objects.create(
            model=self.truck_model1,
            number='truck2',
            type=CargoType.Peace,
            location=area1,
        )

        self.make_calculations()
        list_result, count = self.get_calculated_routes_list()
        self.assertEqual(count, 1)
        result = self.get_calculated_route(list_result[0]['id'])
        self.assertDictEqual(result, {
            **result,
            'truck': truck1.id,
            'cargo': cargo1.id,
            'distance': 10,
            'fuel': 1,
            'path': [area1.id, area2.id],
        })

    def test_multiple_areas_delivery(self):
        area1 = models.Area.objects.create(name='area1')
        area2 = models.Area.objects.create(name='area2')
        area3 = models.Area.objects.create(name='area3')
        area4 = models.Area.objects.create(name='area4')

        models.Route.objects.create(
            wherefrom=area1,
            whereto=area2,
            distance=10,
        )
        models.Route.objects.create(
            wherefrom=area2,
            whereto=area3,
            distance=10,
        )
        models.Route.objects.create(
            wherefrom=area3,
            whereto=area4,
            distance=10,
        )

        truck1 = models.Truck.objects.create(
            model=self.truck_model1,
            number='truck1',
            type=CargoType.Bulk,
            location=area1,
        )
        cargo1 = models.Cargo.objects.create(
            type=CargoType.Bulk,
            location=area1,
            destination=area4,
            mass=100,
        )

        truck2 = models.Truck.objects.create(
            model=self.truck_model1,
            number='truck2',
            type=CargoType.Filler,
            location=area3,
        )
        cargo2 = models.Cargo.objects.create(
            type=CargoType.Filler,
            location=area1,
            destination=area4,
            mass=100,
        )

        self.make_calculations()
        list_result, count = self.get_calculated_routes_list()
        self.assertEqual(count, 2)
        result = self.get_calculated_route(list_result[0]['id'])
        self.assertDictEqual(result, {
            **result,
            'truck': truck1.id,
            'cargo': cargo1.id,
            'distance': 30.0,
            'fuel': 3.0,
            'path': [area1.id, area2.id, area3.id, area4.id],
        })

        result = self.get_calculated_route(list_result[1]['id'])
        self.assertDictEqual(result, {
            **result,
            'truck': truck2.id,
            'cargo': cargo2.id,
            'distance': 50.0,
            'fuel': 5.0,
            'path': [
                area3.id,
                area2.id,
                area1.id,
                area2.id,
                area3.id,
                area4.id,
            ],
        })

    def test_fuel_respects(self):
        area1 = models.Area.objects.create(name='area1')
        area2 = models.Area.objects.create(name='area2')
        area3 = models.Area.objects.create(name='area3')

        # too long for fuel
        models.Route.objects.create(
            wherefrom=area1,
            whereto=area3,
            distance=1200,
        )
        # worse but enough for fuel
        models.Route.objects.create(
            wherefrom=area1,
            whereto=area2,
            distance=700,
        )
        models.Route.objects.create(
            wherefrom=area2,
            whereto=area3,
            distance=900,
        )

        truck1 = models.Truck.objects.create(
            model=self.truck_model1,
            number='truck1',
            type=CargoType.Bulk,
            location=area1,
        )
        cargo1 = models.Cargo.objects.create(
            type=CargoType.Bulk,
            location=area1,
            destination=area3,
            mass=100,
        )

        self.make_calculations()
        list_result, count = self.get_calculated_routes_list()
        self.assertEqual(count, 1)
        result = self.get_calculated_route(list_result[0]['id'])
        self.assertDictEqual(result, {
            **result,
            'truck': truck1.id,
            'cargo': cargo1.id,
            'distance': 1600,
            'fuel': 160,
            'path': [area1.id, area2.id, area3.id],
        })

    def test_truck_cannot_move(self):
        area1 = models.Area.objects.create(name='area1')
        area2 = models.Area.objects.create(name='area2')

        models.Route.objects.create(
            wherefrom=area1,
            whereto=area2,
            distance=1200,
        )

        models.Truck.objects.create(
            model=self.truck_model1,
            number='truck1',
            type=CargoType.Bulk,
            location=area2,
        )
        models.Cargo.objects.create(
            type=CargoType.Bulk,
            location=area1,
            destination=area2,
            mass=100,
        )

        self.make_calculations()
        _, count = self.get_calculated_routes_list()
        self.assertEqual(count, 0)
