import logging
from ontology.models.models import Area, Route, Truck, Cargo, ComputedRoute


logger = logging.getLogger(__name__)


def dijkstra(area_from: Area) -> dict:
    distances = {}
    paths = {}
    checked = {}
    area_ids = Area.objects.values_list('id', flat=True)

    for area_id in area_ids:
        distances[area_id] = float('inf')
        paths[area_id] = []
        checked[area_id] = False

    distances[area_from.id] = 0

    for area in Area.objects.all():
        current_area_id = None

        for looking_area_id in area_ids:
            if not checked[looking_area_id] and (current_area_id is None \
                    or distances[looking_area_id] < distances[current_area_id]):
                current_area_id = looking_area_id
            else:
                continue

            if distances[current_area_id] == float('inf'):
                continue

            checked[current_area_id] = True

            for route in area.wherefrom_routes.union(area.whereto_routes.all()):
                route: Route
                distance = distances[current_area_id] + route.distance
                if distance < distances[route.whereto.id]:
                    distances[route.whereto.id] = distance
                    paths[route.whereto.id] += [current_area_id]

    for area_id in area_ids:
        paths[area_id] += [area_id]

    return distances, paths


def compute_routes():
    computed_routes = []

    for cargo in Cargo.objects.all():
        cargo: Cargo
        logger.info(f'Checking cargo {cargo}')
        suitable_trucks_qs = Truck.objects.filter(
            type=cargo.type,
            model__load_capacity__gte=cargo.mass,
        )
        logger.info(
            f'Calculated {suitable_trucks_qs.count()} suitable trucks: '
            f'{suitable_trucks_qs.values("id", "number")}',
        )

        for truck in suitable_trucks_qs:
            truck: Truck
            computed_route_kwargs = {'cargo': cargo, 'truck': truck}

            truck_to_cargo_distances, truck_to_cargo_paths \
                = dijkstra(truck.location)
            truck_to_cargo_distance, truck_to_cargo_path = (
                truck_to_cargo_distances[cargo.location.id],
                truck_to_cargo_paths[cargo.location.id],
            )
            cargo_to_destination_distances, cargo_to_destination_paths = \
                dijkstra(cargo.location)
            cargo_to_destination_distance, cargo_to_destination_path = (
                cargo_to_destination_distances[cargo.destination.id],
                cargo_to_destination_paths[cargo.destination.id],
            )

            computed_route_kwargs['distance'] = \
                truck_to_cargo_distance \
                + cargo_to_destination_distance
            computed_route_kwargs['fuel'] = \
                computed_route_kwargs['distance'] \
                * truck.model.fuel_consumption \
                / 100
            computed_route_kwargs['path'] = \
                truck_to_cargo_path[:-1] \
                + cargo_to_destination_path

            logger.info(f'Computed route with kwargs: {computed_route_kwargs}')
            computed_routes.append(ComputedRoute(**computed_route_kwargs))

    return computed_routes
