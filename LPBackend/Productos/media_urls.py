"""URLs absolutas para imágenes detrás de un proxy (Render) y /media/."""


def absolute_media_url(request, filefield) -> str:
    if not filefield:
        return ""
    try:
        rel = filefield.url
    except ValueError:
        return ""
    if not rel:
        return ""
    return request.build_absolute_uri(rel)


def producto_imagen_url(request, producto) -> str:
    from django.core.exceptions import ObjectDoesNotExist

    try:
        f = producto.image.imagen
    except ObjectDoesNotExist:
        return ""
    return absolute_media_url(request, f)
