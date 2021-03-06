# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-06-05 15:54
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Flow',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('source_ip', models.GenericIPAddressField()),
                ('protocol', models.SmallIntegerField(choices=[(6, 'TCP'), (17, 'UDP')])),
                ('source_port', models.IntegerField()),
                ('target_port', models.IntegerField()),
                ('risk', models.SmallIntegerField(choices=[(0, 'low'), (1, 'neutral'), (2, 'moderate'), (3, 'high')])),
            ],
        ),
    ]
