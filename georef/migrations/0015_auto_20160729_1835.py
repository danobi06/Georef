# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2016-07-29 18:35
from __future__ import unicode_literals

import deepzoom.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('georef', '0014_auto_20160729_1758'),
    ]

    operations = [
        migrations.AlterField(
            model_name='myimage',
            name='uploaded_image',
            field=models.ImageField(height_field=b'height', max_length=512, upload_to=deepzoom.models.get_uploaded_image_root, width_field=b'width'),
        ),
    ]
