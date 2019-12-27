# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Idea',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('idea_text', models.CharField(max_length=200)),
                ('pub_date', models.DateTimeField(verbose_name='date published')),
            ],
        ),
        migrations.CreateModel(
            name='Innovator',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('innovator_name', models.CharField(max_length=70)),
                ('votes', models.IntegerField(default=0)),
                ('idea', models.ForeignKey(to='idman.Idea')),
            ],
        ),
    ]
