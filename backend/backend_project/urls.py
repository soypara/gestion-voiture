from django.contrib import admin
from django.urls import path, include, re_path
from django.http import HttpResponse
from rest_framework import permissions
from rest_framework.routers import DefaultRouter
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from directions.views import DirectionViewSet  # import correct
from rest_framework_simplejwt.views import TokenRefreshView

def home(request):
    return HttpResponse("Bienvenue sur la page d'accueil !")

# Swagger/OpenAPI
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

# Router pour les directions
router = DefaultRouter()
router.register(r'directions', DirectionViewSet, basename='direction')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('users.urls')),       # users + JWT
    path('api/', include(router.urls)),        # directions CRUD
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path('', home),

    # Swagger / Redoc
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
