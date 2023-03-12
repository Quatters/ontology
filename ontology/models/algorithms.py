import logging
from ontology.models.models import Area, Route, Truck, Cargo, ComputedRoute


logger = logging.getLogger(__name__)


def dijkstra(
    area_from: Area,
    max_straight_distance: float
) -> tuple[dict, dict]:
    distances = {None: float('inf')}
    parents = {}
    checked = {}
    area_ids = Area.objects.values_list('id', flat=True)

    for area_id in area_ids:
        distances[area_id] = float('inf')
        parents[area_id] = None
        checked[area_id] = False

    distances[area_from.id] = 0

    for _ in area_ids:
        current_area_id = None

        for looking_area_id in area_ids:
            if not checked[looking_area_id] and (current_area_id is None \
                    or distances[looking_area_id] < distances[current_area_id]):
                current_area_id = looking_area_id

            if distances[current_area_id] == float('inf'):
                continue

            checked[current_area_id] = True

            area = Area.objects.get(id=current_area_id)
            for route in area.wherefrom_routes.union(area.whereto_routes.all()):
                route: Route
                if route.distance > max_straight_distance:
                    continue
                distance = distances[current_area_id] + route.distance
                if distance < distances[route.whereto.id]:
                    distances[route.whereto.id] = distance
                    parents[route.whereto.id] = current_area_id
                if distance < distances[route.wherefrom.id]:
                    distances[route.wherefrom.id] = distance
                    parents[route.wherefrom.id] = current_area_id

    return distances, parents


def restore_path(area_from: int, area_to: int, parents: dict) -> list[int]:
    if area_from == area_to:
        return []

    current_area_id = area_to
    path = []
    while current_area_id != area_from:
        path += [current_area_id]
        current_area_id = parents[current_area_id]

    path += [area_from]
    return list(reversed(path))


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

            max_straight_distance = truck.model.gas_tank_capacity \
                * 100 \
                / truck.model.fuel_consumption
            truck_to_cargo_distances, truck_to_cargo_parents = \
                dijkstra(truck.location, max_straight_distance)
            truck_to_cargo_distance = \
                truck_to_cargo_distances[cargo.location.id]
            cargo_to_destination_distances, cargo_to_destination_parents = \
                dijkstra(cargo.location, max_straight_distance)
            cargo_to_destination_distance = \
                cargo_to_destination_distances[cargo.destination.id]

            computed_route_kwargs['distance'] = \
                truck_to_cargo_distance \
                + cargo_to_destination_distance
            computed_route_kwargs['fuel'] = \
                computed_route_kwargs['distance'] \
                * truck.model.fuel_consumption \
                / 100
            computed_route_kwargs['path'] = restore_path(
                truck.location.id,
                cargo.location.id,
                truck_to_cargo_parents,
            )[:-1] + restore_path(
                cargo.location.id,
                cargo.destination.id,
                cargo_to_destination_parents,
            )

            logger.info(f'Computed route with kwargs: {computed_route_kwargs}')
            computed_routes.append(ComputedRoute(**computed_route_kwargs))

    return computed_routes
