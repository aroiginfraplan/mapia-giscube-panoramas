# Generated by Django 2.1.5 on 2021-01-19 09:56

import django.contrib.gis.db.models.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mapia_panoramas', '0008_auto_20201228_1003'),
    ]

    operations = [
        migrations.CreateModel(
            name='LocalPointCloud',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=100, unique=True, verbose_name='code')),
                ('name', models.CharField(max_length=100, verbose_name='name')),
                ('file_folder', models.CharField(blank=True, max_length=100, null=True)),
                ('geom', django.contrib.gis.db.models.fields.PolygonField(db_index=True, srid=4326)),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mapia_panoramas.Project', to_field='code')),
            ],
            options={
                'verbose_name': 'Local point cloud',
                'verbose_name_plural': 'Local point clouds',
            },
        ),
    ]