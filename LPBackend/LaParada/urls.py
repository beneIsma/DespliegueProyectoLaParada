from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include("Users.urls")),
    path('api/', include("Productos.urls"))
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
elif settings.SERVE_MEDIA_IN_PRODUCTION:
    # Solo para demos sin CDN; en producción real usa almacenamiento en la nube.
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
