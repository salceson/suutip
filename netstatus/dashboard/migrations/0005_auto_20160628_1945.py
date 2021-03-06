# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-06-28 17:45
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0004_auto_20160605_2125'),
    ]

    operations = [
        migrations.AddField(
            model_name='flow',
            name='source',
            field=models.CharField(blank=True, max_length=64),
        ),
        migrations.AddField(
            model_name='flow',
            name='target',
            field=models.CharField(blank=True, max_length=64),
        ),
        migrations.AlterField(
            model_name='flow',
            name='protocol',
            field=models.SmallIntegerField(choices=[(2054, 'ARP'), (1, 'ICMP'), (6, 'TCP'), (17, 'UDP')]),
        ),
        migrations.AlterField(
            model_name='flow',
            name='risk',
            field=models.SmallIntegerField(choices=[(3, 'high'), (0, 'low'), (2, 'moderate'), (1, 'neutral'), (-1, 'unrated')]),
        ),
    ]
