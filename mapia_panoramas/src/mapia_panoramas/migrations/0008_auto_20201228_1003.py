# Generated by Django 2.1.5 on 2020-12-28 10:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mapia_panoramas', '0007_auto_20201223_0904'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pointcloud',
            name='project',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='pointclouds', to='mapia_panoramas.Project', to_field='code'),
        ),
    ]
