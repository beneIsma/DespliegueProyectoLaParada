from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from Productos.media_urls import producto_imagen_url
from Productos.models import ProductoModel
from rest_framework import status

class ProductosView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):

        productos = ProductoModel.objects.all().order_by("-categoria", "-nombre")

        data = [{
            "nombre": p.nombre,
            "slug": p.slug,
            "categoria": p.categoria.nombre,
            "seccion": p.seccion.nombre,
            "precioCompra": p.precioCompra,
            "precioVenta": p.precioVenta,
            "proveedor": p.proveedor.nombreProveedor,
            "marca": p.marca,
            "descripcion": p.descripcion,
            "imagen": producto_imagen_url(request, p),
        }for p in productos]

        return Response({"data":data, "success": True}, status=status.HTTP_200_OK)

