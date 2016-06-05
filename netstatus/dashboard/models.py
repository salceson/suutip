from django.db import models


# Create your models here.
class Flow(models.Model):
    PROTOCOLS = (
        (6, 'TCP'),
        (17, 'UDP'),
    )

    RISKS = (
        (0, 'low'),
        (1, 'neutral'),
        (2, 'moderate'),
        (3, 'high'),
    )

    date = models.DateTimeField()
    source_ip = models.GenericIPAddressField()
    protocol = models.SmallIntegerField(choices=PROTOCOLS)
    source_port = models.IntegerField()
    target_port = models.IntegerField()
    risk = models.SmallIntegerField(choices=RISKS)
