from collections import defaultdict

from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Product, ProductMaterial, Warehouse
from .serializers import MaterialRequestSerializer


class WareHouserMaterialCheckView(APIView):
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
