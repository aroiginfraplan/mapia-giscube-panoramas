from django.contrib.gis.db import models
from django.utils.translation import gettext as _


class Project(models.Model):
    code = models.CharField(_('code'), max_length=100, blank=False, null=False, unique=True)
    name = models.CharField(_('name'), max_length=100)

    class Meta:
        verbose_name = _('Project')
        verbose_name_plural = _('Projects')

    def __str__(self):
        return '%s' % self.name or self.code


class Panorama(models.Model):
    project = models.ForeignKey(Project, to_field='code', on_delete=models.CASCADE, related_name='panoramas')
    category = models.CharField(max_length=255, null=True, blank=True)
    filename = models.CharField(max_length=100)
    filetype = models.CharField(max_length=20)
    sourceid = models.IntegerField(null=True)
    capture = models.DateTimeField(null=True)
    altitude = models.FloatField(null=False, default=0)
    roll = models.FloatField(null=False, default=0)
    pitch = models.FloatField(null=False, default=0)
    pan = models.FloatField(null=False, default=0)
    geom = models.PointField(db_index=True)

    class Meta:
        verbose_name = _('Panorama')
        verbose_name_plural = _('Panoramas')

    def __str__(self):
        return '%s %s' % (self.project, self.filename)
