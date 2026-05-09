import re

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path, re_path
from django.views.static import serve

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include("Users.urls")),
    path('api/', include("Productos.urls"))
]

if settings.DEBUG:
    # static() solo añade patrones con DEBUG=True.
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
elif getattr(settings, "SERVE_MEDIA_IN_PRODUCTION", False):
    # Con DEBUG=False, django.conf.urls.static.static() devuelve [] (no-op).
    # Hay que registrar /media/ explícitamente para que Render sirva los ficheros.
    _media_prefix = settings.MEDIA_URL.lstrip("/")
    if _media_prefix and not _media_prefix.endswith("/"):
        _media_prefix += "/"
    urlpatterns += [
        re_path(
            r"^%s(?P<path>.*)$" % re.escape(_media_prefix),
            serve,
            {"document_root": str(settings.MEDIA_ROOT)},
        ),
    ]
