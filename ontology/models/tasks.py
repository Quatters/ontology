import logging
from vstutils.tasks import TaskClass
from ontology.models import models
from ontology.wapp import app


logger = logging.getLogger(__name__)


class RouteTask(TaskClass):
    def run(self, *args, **kwargs):
        logger.info('Creating ComputedRoute')
        models.ComputedRoute.objects.create(
            truck_id=1,
            cargo_id=1,
            fuel=1,
            path=[1],
        )


app.register_task(RouteTask())
