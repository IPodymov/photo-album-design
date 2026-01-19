from rest_framework import viewsets, permissions, status, generics
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import ListView

from .models import Album, Photo, Collage, BugReport, UserProfile
from .forms import StyledUserCreationForm, UserForm, ProfileForm
from .serializers import (
    AlbumSerializer,
    PhotoSerializer,
    CollageSerializer,
    UserSerializer,
    UserProfileSerializer,
    ChangePasswordSerializer,
    BugReportSerializer,
)
from .utils import create_collage_image, export_queryset_to_excel
import uuid


class UserOwnedMixin:
    """Миксин для ViewSet'ов с фильтрацией по текущему пользователю."""

    user_field = "user"  # Поле для фильтрации

    def get_queryset(self):
        return self.queryset.filter(**{self.user_field: self.request.user})

    def perform_create(self, serializer):
        serializer.save(**{self.user_field: self.request.user})


# ==================== AUTH VIEWS ====================


class UserRegistrationView(generics.CreateAPIView):
    """Регистрация нового пользователя."""

    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        # Автоматически создаём токен при регистрации
        token, _ = Token.objects.get_or_create(user=user)
        return Response(
            {
                "user": UserProfileSerializer(user).data,
                "token": token.key,
                "message": "Регистрация успешна!",
            },
            status=status.HTTP_201_CREATED,
        )


class UserLogoutView(APIView):
    """Выход пользователя (удаление токена)."""

    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        # Удаляем токен пользователя
        request.user.auth_token.delete()
        return Response({"message": "Вы успешно вышли из системы."}, status=status.HTTP_200_OK)


class UserProfileView(generics.RetrieveUpdateAPIView):
    """Просмотр и обновление профиля текущего пользователя."""

    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user


class ChangePasswordView(generics.UpdateAPIView):
    """Смена пароля текущего пользователя."""

    serializer_class = ChangePasswordSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user

    def update(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = self.get_object()
        user.set_password(serializer.validated_data["new_password"])
        user.save()

        # Обновляем токен после смены пароля
        Token.objects.filter(user=user).delete()
        new_token = Token.objects.create(user=user)

        return Response(
            {"message": "Пароль успешно изменён.", "token": new_token.key},
            status=status.HTTP_200_OK,
        )


class AlbumViewSet(UserOwnedMixin, viewsets.ModelViewSet):
    queryset = Album.objects.all()
    serializer_class = AlbumSerializer
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=True, methods=["post"], url_path="upload-photos")
    def upload_photos(self, request, pk=None):
        album = self.get_object()
        images = request.FILES.getlist("images")  # Expecting key 'images'

        if not images:
            return Response({"error": "No images provided"}, status=status.HTTP_400_BAD_REQUEST)

        created_photos = []
        for image in images:
            photo = Photo.objects.create(album=album, image=image)
            created_photos.append(photo)

        return Response(
            {"status": "Photos uploaded", "count": len(created_photos)},
            status=status.HTTP_201_CREATED,
        )

    @action(detail=True, methods=["post"], url_path="generate-collage")
    def generate_collage(self, request, pk=None):
        album = self.get_object()

        # "Generate based on best shots"
        # We look for photos marked as favorite first
        # use_best = request.data.get("use_best_shots", False)  # Optional flag from frontend

        photos = album.photos.all()

        # If user explicitly wants best shots, or just as a default logic if we decide:
        # Let's say if we have favorites, we use them. If not, we use all.
        favorites = photos.filter(is_favorite=True)
        if favorites.exists():
            photos_to_use = favorites
        else:
            photos_to_use = photos

        if not photos_to_use.exists():
            return Response(
                {"error": "No photos in album to generate collage"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        collage_file = create_collage_image(photos_to_use)

        if collage_file:
            collage = Collage(album=album)
            collage.image.save(f"collage_{uuid.uuid4()}.jpg", collage_file)
            serializer = CollageSerializer(collage)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(
                {"error": "Failed to generate collage"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class PhotoViewSet(UserOwnedMixin, viewsets.ModelViewSet):
    """Управление фотографиями (удаление, просмотр, пометка избранным)."""

    queryset = Photo.objects.all()
    serializer_class = PhotoSerializer
    permission_classes = [permissions.IsAuthenticated]
    user_field = "album__user"  # Переопределяем поле фильтрации

    def perform_create(self, serializer):
        # Фото создаются через upload_photos в AlbumViewSet
        serializer.save()


class BugReportViewSet(UserOwnedMixin, viewsets.ModelViewSet):
    queryset = BugReport.objects.all()
    serializer_class = BugReportSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Админ видит все, пользователь — только свои
        if self.request.user.is_staff:
            return BugReport.objects.all()
        return super().get_queryset()

    @action(
        detail=False,
        methods=["get"],
        permission_classes=[permissions.IsAdminUser],
        url_path="export-excel",
    )
    def export_excel(self, request):
        """Экспорт баг-репортов в Excel (только для админа)."""
        headers = ["ID", "User", "Title", "Description", "Status", "Created At"]

        def extract_row(report):
            return [
                str(report.id),
                report.user.username,
                report.title,
                report.description,
                report.status,
                report.created_at.strftime("%Y-%m-%d %H:%M:%S"),
            ]

        return export_queryset_to_excel(
            queryset=BugReport.objects.all(),
            headers=headers,
            row_extractor=extract_row,
            sheet_title="Bug Reports",
            filename_prefix="bug_reports",
        )


# ==================== WEB AUTH VIEWS ====================


def register_view(request):
    if request.method == "POST":
        form = StyledUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("home")
    else:
        form = StyledUserCreationForm()
    return render(request, "auth/register.html", {"form": form})


@method_decorator(login_required, name="dispatch")
class DashboardView(ListView):
    model = Album
    template_name = "dashboard/index.html"
    context_object_name = "albums"

    def get_queryset(self):
        return Album.objects.filter(user=self.request.user).order_by("-created_at")


@login_required
def create_album_view(request):
    if request.method == "POST":
        title = request.POST.get("title")
        description = request.POST.get("description")
        photos = request.FILES.getlist("photos")

        album = Album.objects.create(user=request.user, title=title, description=description)

        for photo in photos:
            Photo.objects.create(album=album, image=photo)

        return redirect("dashboard")

    return render(request, "dashboard/create_album.html")


@login_required
def edit_profile_view(request):
    try:
        request.user.profile
    except UserProfile.DoesNotExist:
        UserProfile.objects.create(user=request.user)

    if request.method == "POST":
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = ProfileForm(request.POST, request.FILES, instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, "Ваш профиль был успешно обновлен!")
            return redirect("profile")
        else:
            messages.error(request, "Пожалуйста, исправьте ошибки ниже.")
    else:
        user_form = UserForm(instance=request.user)
        profile_form = ProfileForm(instance=request.user.profile)
    return render(
        request, "dashboard/profile.html", {"user_form": user_form, "profile_form": profile_form}
    )


@login_required
def profile_view(request):
    try:
        request.user.profile
    except UserProfile.DoesNotExist:
        UserProfile.objects.create(user=request.user)

    return render(request, "dashboard/profile_view.html", {"user": request.user})
