# Generated by Django 2.1.7 on 2022-09-03 05:23

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_id', models.CharField(max_length=34, unique=True)),
                ('x_open', models.SmallIntegerField(default=0, validators=[django.core.validators.MinValueValidator(0)])),
                ('y_open', models.SmallIntegerField(default=0, validators=[django.core.validators.MinValueValidator(0)])),
                ('z_open', models.SmallIntegerField(default=0, validators=[django.core.validators.MinValueValidator(0)])),
                ('x_close', models.SmallIntegerField(default=0, validators=[django.core.validators.MinValueValidator(0)])),
                ('y_close', models.SmallIntegerField(default=0, validators=[django.core.validators.MinValueValidator(0)])),
                ('z_close', models.SmallIntegerField(default=0, validators=[django.core.validators.MinValueValidator(0)])),
            ],
        ),
    ]
