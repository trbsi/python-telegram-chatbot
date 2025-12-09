from django.contrib import admin
from django.contrib import messages
from django.db.models import QuerySet
from django.http import HttpRequest
from django.utils.html import format_html

from src.media.enums.media_status_enum import MediaStatusEnum
from src.media.models import Media


@admin.register(Media)
class AdminMedia(admin.ModelAdmin):
    list_filter = ['created_at', 'status', 'is_approved']
    list_display = ('id', 'is_approved', 'user', 'file_preview', 'status', 'created_at')
    fields = (
        'user',
        'is_processed',
        'is_approved',
        'file_type',
        'status',
        'description',
        'file_preview',
        'trailer',
        'thumbnail',
    )
    readonly_fields = ('created_at', 'file_preview', 'trailer', 'thumbnail')
    search_fields = ('user__username',)
    actions = ['mark_as_approved_multiple', 'mark_as_deleted_multiple', ]

    def has_delete_permission(self, request, obj=None):
        return False

    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']

        return actions

    @admin.action(description='Mark as approved multiple')
    def mark_as_approved_multiple(self, request: HttpRequest, queryset: QuerySet):
        queryset.update(is_approved=True)
        self.message_user(request, 'Approved', messages.SUCCESS)

    @admin.action(description='Mark as deleted multiple')
    def mark_as_deleted_multiple(self, request: HttpRequest, queryset: QuerySet):
        queryset.update(status=MediaStatusEnum.STATUS_DELETED.value)
        self.message_user(request, 'Deleted', messages.SUCCESS)

    @admin.action(description="Mark as deleted", )
    def mark_as_deleted_single(self, request: HttpRequest, media):
        media.status = MediaStatusEnum.STATUS_DELETED.value
        media.save()
        messages.success(request, "Media deleted")

    @admin.display(description="File")
    def file_preview(self, media: Media) -> str | None:
        if media.is_image():
            return format_html(
                '<img style="max-width: 300px" src="{media}">',
                media=media.get_file_url()
            )
        if media.is_video():
            return format_html(
                '<video style="max-width: 300px" controls  preload="none"><source src="{media}"></video>',
                media=media.get_file_url()
            )

        return None

    @admin.display(description="Thumbnail")
    def thumbnail(self, media: Media) -> str | None:
        if media.file_thumbnail is None:
            return None

        return format_html(
            '<img src="{media}">',
            media=media.get_thumbnail_url()
        )

    @admin.display(description="Trailer")
    def trailer(self, media: Media) -> str | None:
        if media.file_trailer is None:
            return None

        return format_html(
            '<video controls><source src="{media}"></video>',
            media=media.get_trailer_url()
        )
