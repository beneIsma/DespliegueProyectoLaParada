"""URLs absolutas para imágenes detrás de un proxy (Render) y sustituto si falta el fichero."""

from pathlib import Path

from django.conf import settings


def _absolute(request, path: str) -> str:
    """path empieza por / (ej. /media/... o /static/...)."""
    path = path or ""
    if not path.startswith("/"):
        path = "/" + path
    base = getattr(settings, "PUBLIC_BASE_URL", "") or ""
    base = base.strip().rstrip("/")
    if base:
        return f"{base}{path}"
    return request.build_absolute_uri(path)


def _placeholder(request) -> str:
    return _absolute(request, "/static/placeholders/no-imagen.png")


def absolute_media_url(request, filefield) -> str:
    if not filefield:
        return _placeholder(request)
    try:
        rel = filefield.url
    except ValueError:
        return _placeholder(request)
    if not rel:
        return _placeholder(request)

    try:
        disk_path = Path(filefield.path)
        if not disk_path.is_file():
            return _placeholder(request)
    except (ValueError, AttributeError, OSError):
        pass

    return _absolute(request, rel)


def producto_imagen_url(request, producto) -> str:
    from django.core.exceptions import ObjectDoesNotExist

    try:
        f = producto.image.imagen
    except ObjectDoesNotExist:
        return _placeholder(request)
    return absolute_media_url(request, f)
