from django.contrib import admin
from .models import Album, Photo, Collage, BugReport
from .utils import export_queryset_to_excel


class PhotoInline(admin.TabularInline):
    model = Photo
    extra = 1


class AlbumAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'created_at')
    inlines = [PhotoInline]


@admin.register(BugReport)
class BugReportAdmin(admin.ModelAdmin):
    list_display = ("title", "user", "status", "created_at")
    list_filter = ("status", "created_at")
    search_fields = ("title", "description", "user__username")
    actions = ["export_to_excel"]

    @admin.action(description="Экспорт выбранных баг-репортов в Excel")
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


admin.site.register(Album, AlbumAdmin)
admin.site.register(Photo)
admin.site.register(Collage)

