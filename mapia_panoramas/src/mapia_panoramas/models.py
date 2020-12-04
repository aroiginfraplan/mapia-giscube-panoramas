from django.contrib.gis.db import models
from django.utils.translation import gettext as _


class Project(models.Model):
    code = models.CharField(_('code'), max_length=100, blank=False, null=False, unique=True)
    name = models.CharField(_('name'), max_length=100)
    folder_panorama = models.CharField(max_length=100, null=True, blank=True)
    folder_images = models.CharField(max_length=100, null=True, blank=True)
    folder_point_cloud = models.CharField(max_length=100, null=True, blank=True)

    class Meta:
        verbose_name = _('Campaign')
        verbose_name_plural = _('Campaigns')

    def __str__(self):
        return '%s' % self.name or self.code


class Panorama(models.Model):
    project = models.ForeignKey(Project, to_field='code', on_delete=models.CASCADE, related_name='panoramas')
    category = models.CharField(max_length=255, null=True, blank=True)
    file_name = models.CharField(max_length=100, null=True, blank=True)
    file_folder = models.CharField(max_length=100, null=True, blank=True)
    file_type = models.CharField(max_length=20, null=True, blank=True)
    source_id = models.IntegerField(null=True)
    date = models.DateTimeField(null=True)
    altitude = models.FloatField(null=False, default=0)
    pan = models.FloatField(null=False, default=0)
    pitch = models.FloatField(null=False, default=0)
    roll = models.FloatField(null=False, default=0)
    geom = models.PointField(db_index=True)

    class Meta:
        verbose_name = _('Panorama')
        verbose_name_plural = _('Panoramas')

    def __str__(self):
        return '%s %s' % (self.project, self.file_name)


class Lateral(models.Model):
    panorama = models.ForeignKey(Panorama, on_delete=models.CASCADE, related_name='laterals')
    file_name = models.CharField(max_length=100, null=False)
    file_folder = models.CharField(max_length=100, null=True, blank=True)
    file_type = models.CharField(max_length=20, null=True, blank=True)
    pan = models.FloatField(null=False, default=0)

    class Meta:
        verbose_name = _('Lateral image')
        verbose_name_plural = _('Lateral images')

    def __srt__(self):
        return '%s %s' % (self.file_name, self.panorama)

class PointCloud(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    code = models.CharField(_('code'), max_length=100, blank=False, null=False, unique=True)
    name = models.CharField(_('name'), max_length=100)
    file_folder = models.CharField(max_length=100, null=True, blank=True)
    geom = models.PolygonField(db_index=True)

    class Meta:
        verbose_name = _('Point cloud')
        verbose_name_plural = _('Point clouds')

    def __str__(self):
        return '%s %s' % (self.name, self.project)
