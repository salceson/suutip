from enum import Enum
import inspect

from django.db import models


class ChoiceEnum(Enum):
    @classmethod
    def choices(cls):
        members = inspect.getmembers(cls, lambda m: not(inspect.isroutine(m)))
        props = [m for m in members if not(m[0][:2] == '__')]
        choices = tuple([(p[1].value, p[1].name) for p in props])
        return choices


class Protocols(ChoiceEnum):
    ARP = 0x806
    ICMP = 1
    TCP = 6
    UDP = 17


class Risks(ChoiceEnum):
    unrated = -1
    low = 0
    neutral = 1
    moderate = 2
    high = 3


# Create your models here.
class Flow(models.Model):
    date = models.DateTimeField()
    source_ip = models.GenericIPAddressField()
    target_ip = models.GenericIPAddressField()
    protocol = models.SmallIntegerField(choices=Protocols.choices())
    source_port = models.IntegerField()
    target_port = models.IntegerField()
    risk = models.SmallIntegerField(choices=Risks.choices())
