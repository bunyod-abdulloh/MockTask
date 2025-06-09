from django.urls import path

from .views import WareHouserMaterialCheckView, ProductListCreateView, MaterialListCreateView, \
    ProductMaterialListCreateView, WarehouseListCreateView

urlpatterns = [
    path('products/', ProductListCreateView.as_view()),
    path('materials/', MaterialListCreateView.as_view()),
    path('product-materials/', ProductMaterialListCreateView.as_view()),
    path('warehouses/', WarehouseListCreateView.as_view()),
    path('warehouse-check/', WareHouserMaterialCheckView.as_view()),
]
