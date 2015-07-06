# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Log',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('level', models.CharField(max_length=10)),
                ('msg', models.TextField()),
                ('datetime', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'ordering': ['-datetime'],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='MonitoringObject',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('key', models.CharField(max_length=255)),
                ('alarm', models.IntegerField(default=0)),
                ('alarm_num', models.IntegerField(default=0)),
                ('alarm_sub', models.TextField(blank=True)),
                ('alarm_msg', models.TextField(blank=True)),
                ('checked', models.DateTimeField(default=b'2014-01-01 00:01')),
            ],
            options={
                'permissions': (('list_monitoringobject', 'Can list monitoringobject'),),
            },
            bases=(models.Model,),
        ),
    ]
