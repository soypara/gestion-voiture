from django.contrib import admin
from django.urls import path, include, re_path
from django.http import HttpResponse
from rest_framework import permissions, routers
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework_simplejwt.views import TokenRefreshView
from detenteurs.views import DetenteurViewSet  # Assure-toi d'importer le ViewSet

def home(request):
    return HttpResponse("Bienvenue sur la page d'accueil !")

# Swagger
schema_view = get_schema_view(
   openapi.Info(
      title="API Documentation",
      default_version='v1',
      description="API Swagger pour ton projet Django",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="support@example.com"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

# 🔹 ROUTER pour DRF
router = routers.DefaultRouter()
router.register(r"detenteurs", DetenteurViewSet, basename="detenteur")

urlpatterns = [
    path('admin/', admin.site.urls),

    # USERS + JWT
    path('api/', include('users.urls')),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # DIRECTIONS
    path('api/', include('directions.urls')),

    # VOITURES 
    path('api/', include('voitures.urls')),

    # DETENTEURS via router
    path('api/', include(router.urls)),

    path('', home),

    # SWAGGER
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
'''from django.contrib import admin
from django.urls import path, include, re_path
from django.http import HttpResponse
from rest_framework import permissions, routers
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework_simplejwt.views import TokenRefreshView

from detenteurs.views import DetenteurViewSet

def home(request):
    return HttpResponse("Bienvenue sur la page d'accueil !")

# 🔹 Swagger
schema_view = get_schema_view(
   openapi.Info(
      title="API Documentation",
      default_version='v1',
      description="API Swagger pour ton projet Django",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="support@example.com"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

'''