# Generated by Django 2.2.11 on 2020-04-15 10:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mapia_panoramas', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='project',
            options={'verbose_name': 'Project', 'verbose_name_plural': 'Projects'},
        ),
        migrations.AddField(
            model_name='panorama',
            name='category',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
