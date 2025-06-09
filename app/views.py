from collections import defaultdict

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Product, ProductMaterial, Warehouse, Material
from .serializers import MaterialRequestSerializer, ProductSerializer, ProductMaterialSerializer, WarehouseSerializer, \
    MaterialSerializer


class ProductListCreateView(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class MaterialListCreateView(generics.ListCreateAPIView):
    queryset = Material.objects.all()
    serializer_class = MaterialSerializer


class ProductMaterialListCreateView(generics.ListCreateAPIView):
    queryset = ProductMaterial.objects.all()
    serializer_class = ProductMaterialSerializer


class WarehouseListCreateView(generics.ListCreateAPIView):
    queryset = Warehouse.objects.all()
    serializer_class = WarehouseSerializer

class WareHouserMaterialCheckView(APIView):

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_ARRAY,
            items=openapi.Schema(  # Bu yerda Items emas, Schema bo'lishi kerak!
                type=openapi.TYPE_OBJECT,
                properties={
                    'product_code': openapi.Schema(type=openapi.TYPE_INTEGER, example=1001),
                    'quantity': openapi.Schema(type=openapi.TYPE_INTEGER, example=3),
                },
                required=['product_code', 'quantity']
            ),
            example=[
                {"product_code": 1001, "quantity": 3},
                {"product_code": 1002, "quantity": 5}
            ]
        )
    )
    def post(self, request):
        serializer = MaterialRequestSerializer(data=request.data, many=True)
        serializer.is_valid(raise_exception=True)

        product_requests = serializer.validated_data
        user_materials = defaultdict(float)

        results = []

        for req in product_requests:
            product = Product.objects.get(code=req['product_code'])
            qty_needed = req['quantity']

            product_materials = ProductMaterial.objects.filter(
                product=product
            )

            product_result = {
                "product_name": product.name,
                "product_qty": qty_needed,
                "product_materials": []
            }

            for pm in product_materials:
                material_id = pm.material.id
                total_needed = pm.quantity * qty_needed
                total_needed -= user_materials[material_id]

                warehouses = Warehouse.objects.filter(
                    material_id=material_id
                ).order_by('id')

                for warehouse in warehouses:
                    if total_needed <= 0:
                        break

                    take_qty = min(warehouse.remainder, total_needed)

                    if take_qty > 0:
                        product_result['product_materials'].append({
                            "warehouse_id": warehouse.id,
                            "material_name": pm.material.name,
                            "qty": take_qty,
                            "price": warehouse.price
                        })
                        user_materials[material_id] += take_qty
                        total_needed -= take_qty

                # If still not enough material, add missing
                if total_needed > 0:
                    product_result['product_materials'].append({
                        "warehouse_id": None,
                        "material_name": pm.material.name,
                        "qty": total_needed,
                        "price": None
                    })
                    user_materials[material_id] += total_needed
            results.append(product_result)
        data = {
            "result": results
        }
        return Response(data=data)
