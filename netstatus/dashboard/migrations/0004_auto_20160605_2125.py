# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-06-05 21:25
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0003_flow_target_ip'),
    ]

    operations = [
        migrations.AlterField(
            model_name='flow',
            name='risk',
            field=models.SmallIntegerField(choices=[(0, 'neutral'), (1, 'low'), (2, 'moderate'), (3, 'high')]),
        ),
    ]
