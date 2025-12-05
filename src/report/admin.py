from django.contrib import admin
from django.urls import reverse_lazy
from django.utils.html import format_html

from src.core.utils import reverse_lazy_admin
from src.media.models import Media
from src.report.models import Report
from src.user.models import User


@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    list_filter = ('status',)
    list_display = ('content_object', 'status', 'created_at')
    fields = (
        'content_object',
        'description',
        'status',
        'reported_by',
        'get_content',
    )
    readonly_fields = ('get_content', 'content_object')

    @admin.display(description="Content")
    def get_content(self, report: Report):
        if report.is_user():
            user: User = report.content_object
            href = reverse_lazy('user.profile', kwargs={'username': user.username})
            return format_html(f'<a class="underline" href="{href}">View user</a>', )

        if report.is_media():
            media: Media = report.content_object
            media_url = media.get_file_url()

            if media.is_image():
                return format_html(f'<img src="{media_url}">')
            if media.is_video():
                admin_media_url = reverse_lazy_admin(object=media, action='change', args=[media.id])
                return format_html(
                    f'<div class="flex mb-5"><a href="{admin_media_url}" class="bg-blue-600 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded">View media</a></div>'
                    f'<div> <video controls><source src="{media_url}"></video></div>'
                )
        return ''
