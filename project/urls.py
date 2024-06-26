"""project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from core.viewsets import BrandViewSet
from core.viewsets.AuthViewSet import AuthViewSet
from core.viewsets.ManufacturerViewSet import ManufacturerViewSet
from core.viewsets.VehicleUnitViewSet import VehicleUnitViewSet
from core.viewsets.VehicleViewSet import VehicleViewSet
from django.conf.urls.static import static
from django.conf import settings

from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

router = routers.SimpleRouter()

router.register('brands', BrandViewSet, basename='brands')
router.register('manufacturers', ManufacturerViewSet, basename='manufacturers')
router.register('vehicles', VehicleViewSet, basename='vehicles')
router.register('vehicle-units', VehicleUnitViewSet, basename='vehicle-units')
router.register('auth', AuthViewSet, basename='auth')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('api/auth/login-check/', TokenObtainPairView.as_view(), name='token-obtain-pair'),
    path('api/auth/token-refresh/', TokenRefreshView.as_view(), name='token-refresh'),

    # API Documentation
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
