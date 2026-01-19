from PIL import Image
import math
from io import BytesIO
from django.core.files.base import ContentFile
from django.http import HttpResponse
from datetime import datetime
import openpyxl

# Константы для коллажей
COLLAGE_CELL_SIZE = 300
COLLAGE_BG_COLOR = "white"
COLLAGE_FORMAT = "JPEG"


def load_and_resize_image(image_path, size):
    """Загружает и изменяет размер изображения."""
    img = Image.open(image_path)
    img.thumbnail(size)
    return img.resize(size)


def calculate_grid(count):
    """Вычисляет размеры сетки для коллажа."""
    cols = math.ceil(math.sqrt(count))
    rows = math.ceil(count / cols)
    return cols, rows


def create_collage_image(photos, cell_size=COLLAGE_CELL_SIZE, output_format=COLLAGE_FORMAT):
    """Создаёт коллаж из списка фотографий."""
    if not photos:
        return None

    # Загрузка и изменение размера изображений
    pil_images = []
    for photo in photos:
        try:
            img = load_and_resize_image(photo.image.path, (cell_size, cell_size))
            pil_images.append(img)
        except Exception as e:
            print(f"Error opening image {photo.id}: {e}")
            continue

    if not pil_images:
        return None

    # Расчёт сетки
    cols, rows = calculate_grid(len(pil_images))
    collage_width = cols * cell_size
    collage_height = rows * cell_size

    # Создание коллажа
    mode = "RGB" if output_format == "JPEG" else "RGBA"
    bg_color = COLLAGE_BG_COLOR if output_format == "JPEG" else (255, 255, 255, 0) # Transparent for PNG or White? User didn't specify, but white is safer as transparency can be weird for collages. Let's stick to user request "png format". Usually PNG implies transparency support, but for photo album collage white bg is standard. I'll keep white bg but format PNG.
    
    collage = Image.new(mode, (collage_width, collage_height), COLLAGE_BG_COLOR)

    for i, img in enumerate(pil_images):
        x = (i % cols) * cell_size
        y = (i // cols) * cell_size
        collage.paste(img, (x, y))

    buffer = BytesIO()
    collage.save(buffer, format=output_format)
    ext = "jpg" if output_format == "JPEG" else output_format.lower()
    return ContentFile(buffer.getvalue(), name=f"collage.{ext}")


def export_queryset_to_excel(queryset, headers, row_extractor, sheet_title, filename_prefix):
    """
    Универсальная функция экспорта QuerySet в Excel.

    Args:
        queryset: QuerySet для экспорта
        headers: список заголовков столбцов
        row_extractor: функция (obj) -> list, извлекающая данные строки
        sheet_title: название листа Excel
        filename_prefix: префикс имени файла

    Returns:
        HttpResponse с Excel файлом
    """
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = sheet_title

    ws.append(headers)

    for obj in queryset:
        ws.append(row_extractor(obj))

    response = HttpResponse(
        content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
    response["Content-Disposition"] = (
        f'attachment; filename={filename_prefix}_{datetime.now().strftime("%Y%m%d")}.xlsx'
    )
    wb.save(response)
    return response
