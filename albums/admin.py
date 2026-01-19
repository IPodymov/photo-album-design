from django.contrib import admin
from .models import Album, Photo, Collage, BugReport


class PhotoInline(admin.TabularInline):
    model = Photo
    extra = 1


class AlbumAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'created_at')
    inlines = [PhotoInline]


admin.site.register(Album, AlbumAdmin)
admin.site.register(Photo)
admin.site.register(Collage)
admin.site.register(BugReport)
