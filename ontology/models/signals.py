from django.db.models import signals
from django.dispatch import receiver
from django.db.utils import IntegrityError
from ontology.models import models


@receiver(signals.pre_save, sender=models.Route)
def check_whereto_wherefrom(instance: models.Route, **kwargs):
    analogue_routes = models.Route.objects.filter(
        wherefrom=instance.whereto,
        whereto=instance.wherefrom
    )

    if analogue_routes.exists():
        raise IntegrityError
