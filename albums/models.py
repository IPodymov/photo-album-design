from django.db import models
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField
import uuid


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    avatar = CloudinaryField('avatar', blank=True, null=True)
    bio = models.TextField(max_length=500, blank=True)
    location = models.CharField(max_length=30, blank=True)
    birth_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.user.username}'s profile"


def get_album_media_path(user_id, album_id, subfolder, filename):
    """Общая функция для формирования путей медиафайлов альбома."""
    return f"user_{user_id}/album_{album_id}/{subfolder}/{filename}"


def photo_directory_path(instance, filename):
    """Путь для загрузки фотографий."""
    return get_album_media_path(
        instance.album.user.id, instance.album.id, "photos", filename
    )


def collage_directory_path(instance, filename):
    """Путь для загрузки коллажей."""
    return get_album_media_path(
        instance.album.user.id, instance.album.id, "collages", filename
    )


class Album(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="albums")
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} ({self.user.username})"


class Photo(models.Model):
    album = models.ForeignKey(Album, on_delete=models.CASCADE, related_name="photos")
    image = models.ImageField(upload_to=photo_directory_path)
    created_at = models.DateTimeField(auto_now_add=True)
    is_favorite = models.BooleanField(default=False)  # For 'best shots' feature

    def __str__(self):
        return f"Photo {self.id} in {self.album.title}"


class Collage(models.Model):
    album = models.ForeignKey(Album, on_delete=models.CASCADE, related_name="collages")
    image = models.ImageField(upload_to=collage_directory_path)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Collage {self.id} for {self.album.title}"


class BugReport(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bug_reports", null=True, blank=True)
    title = models.CharField(max_length=255)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=20, default="open", choices=[("open", "Open"), ("closed", "Closed")]
    )

    def __str__(self):
        return f"Bug: {self.title} ({self.status})"
