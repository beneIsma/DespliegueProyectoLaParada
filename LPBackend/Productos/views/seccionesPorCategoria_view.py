from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from Productos.media_urls import absolute_media_url
from Productos.models import SeccionesCategoria


class SeccionesPorCategoriaView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        secciones = SeccionesCategoria.objects.all().order_by('-categoria')
        data = [{
                "categoria": s.categoria.nombre,
                "nombre": s.nombre,
                "imagen": absolute_media_url(request, s.imagen),
            }for s in secciones]

        return Response({"data":data, "success":True}, status=status.HTTP_200_OK)