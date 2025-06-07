from django.urls import path

from .views import WareHouserMaterialCheckView

urlpatterns = [
    path('', WareHouserMaterialCheckView.as_view(), ),
]
