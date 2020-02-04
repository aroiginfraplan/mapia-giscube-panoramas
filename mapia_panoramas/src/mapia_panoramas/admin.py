from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from django.utils.translation import gettext as _

from .models import Project


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'get_url',)
    list_display_links = list_display
    search_fields = list_display
    readonly_fields = ('get_url',)

    def get_url(self, obj):
        text = '-'
        try:
            if obj:
                url = reverse('projects-panoramas', args=[obj.code])
                text = format_html('<a href="{url}" target="_blank">{text}</a>', url=url, text=_('View'))
        except Exception:
            pass
        return text
    get_url.short_description = _('URL')
