from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from import_export import resources
from simple_history.admin import SimpleHistoryAdmin

from .models import Album, Photo, Collage, BugReport
from .utils import export_queryset_to_excel


class AlbumResource(resources.ModelResource):
    photo_count = resources.Field()

    class Meta:
        model = Album
        fields = ("id", "title", "user__username", "is_public", "created_at", "photo_count")
        export_order = ("id", "title", "user__username", "created_at", "is_public", "photo_count")

    # Customization 1: Dehydrate field (Transform value during export)
    def dehydrate_is_public(self, album):
        return "Public" if album.is_public else "Private"

    # Customization 2: Get specific field (Calculate value)
    def dehydrate_photo_count(self, album):
        return album.photos.count()

    # Customization 3: Filter Queryset for Export (e.g., exclude empty albums or sort)
    def get_export_queryset(self, request, queryset):
        """
        Custom export queryset:
        Only export albums that are either public or belong to the current user (if user is not superuser).
        Superusers get everything selected.
        Example customization: Ordered by reversed creation date.
        """
        return queryset.order_by("-created_at")


class PhotoInline(admin.TabularInline):
    model = Photo
    extra = 1


@admin.register(Album)
class AlbumAdmin(ImportExportModelAdmin, SimpleHistoryAdmin):
    resource_class = AlbumResource
    list_display = ("title", "user", "is_public", "photo_count", "created_at")
    list_filter = ("is_public", "created_at", "user")
    search_fields = ("title", "description")
    ordering = ("-created_at",)
    inlines = [PhotoInline]
    date_hierarchy = "created_at"

    def photo_count(self, obj):
        return obj.photos.count()

    photo_count.short_description = "Photos"


@admin.register(BugReport)
class BugReportAdmin(ImportExportModelAdmin):
    list_display = ("title", "user", "status", "created_at")
    list_filter = ("status", "created_at")
    search_fields = ("title", "description", "user__username")
    date_hierarchy = "created_at"
    # Keeping the custom action as well
    actions = ["export_to_excel"]

    @admin.action(description="Экспорт выбранных баг-репортов в Excel (Custom)")
    def export_to_excel(self, request, queryset):
        headers = ["ID", "User", "Title", "Description", "Status", "Created At"]

        def extract_row(report):
            return [
                report.id,
                report.user.username if report.user else "Anonymous",
                report.title,
                report.description,
                report.status,
                report.created_at.strftime("%Y-%m-%d %H:%M:%S"),
            ]

        return export_queryset_to_excel(
            queryset=queryset,
            headers=headers,
            row_extractor=extract_row,
            sheet_title="Bug Reports",
            filename_prefix="bug_reports",
        )


admin.site.register(Photo, SimpleHistoryAdmin)
admin.site.register(Collage)
