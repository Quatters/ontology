import os
from vstutils.settings import *  # noqa: F403

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, "media")

SPA_STATIC.append({'priority': 10, 'type': 'js', 'name': 'ontology/bundle/app.js'})

INSTALLED_APPS += [  # noqa: F405
    'ontology',
]

LANGUAGES = (
    ('en', 'English'),
    ('ru', 'Русский'),
)

API[VST_API_VERSION] = {
    'statistics': {
        'view': 'ontology.api.StatisticsViewSet',
    },
    'delivery_areas': {
        'view': 'ontology.api.AreaViewSet',
    },
    'routes': {
        'view': 'ontology.api.RouteViewSet',
    },
    'truck_models': {
        'view': 'ontology.api.TruckModelViewSet',
    },
    'trucks': {
        'view': 'ontology.api.TruckViewSet',
    },
    'cargos': {
        'view': 'ontology.api.CargoViewSet',
    },
    'computed_routes': {
        'view': 'ontology.api.ComputedRouteViewSet',
    },
}

PROJECT_GUI_MENU = [
    {
        'name': 'Knowledge editor',
        'span_class': 'fa fa-book',
        'sublinks': [
            {
                'name': 'Delivery areas',
                'url': '/delivery_areas',
                'span_class': 'fa fa-location-arrow',
            },
            {
                'name': 'Routes',
                'url': '/routes',
                'span_class': 'fa fa-road',
            },
            {
                'name': 'Truck models',
                'url': '/truck_models',
                'span_class': 'fa fa-cog',
            },
            {
                'name': 'Trucks',
                'url': '/trucks',
                'span_class': 'fa fa-truck',
            },
        ],
    },
    {
        'name': 'Data editor',
        'span_class': 'fa fa-database',
        'url': '/cargos',
    },
    {
        'name': 'Problem solver',
        'span_class': 'fa fa-calculator',
        'url': '/computed_routes',
    }
]

CELERY_TASK_SERIALIZER = 'json'
CELERY_ACCEPT_CONTENT = ['json']
CELERY_RESULT_SERIALIZER = 'json'
