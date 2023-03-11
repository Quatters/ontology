import logging
from django.db import transaction
from vstutils.tasks import TaskClass
from ontology.models import models
from ontology.models.algorithms import compute_routes
from ontology.wapp import app


logger = logging.getLogger(__name__)


class RouteTask(TaskClass):
    @transaction.atomic
    def run(self, *args, **kwargs):
        routes = compute_routes()
        models.ComputedRoute.objects.all().delete()
        for route in routes:
            route.save()


app.register_task(RouteTask())
