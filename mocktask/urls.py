
from django.contrib import admin
from django.urls import path, include
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

urlpatterns = [
    path('admin/', admin.site.urls),
    path('wrhs/', include('app.urls')),
]

schema_view = get_schema_view(
    openapi.Info(title="Omborxona API", default_version='v1'),
    public=True,
    permission_classes=[permissions.AllowAny, ],
)

urlpatterns += [
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
]
