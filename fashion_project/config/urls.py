"""
URL configuration for config project.
"""
from django.contrib import admin
from django.urls import path, include 
from rest_framework.routers import DefaultRouter 
from catalogue.views import stats_view, GarmentViewSet, DesignerViewSet, TrendViewSet 

router = DefaultRouter()
router.register(r'garments', GarmentViewSet)
router.register(r'designers', DesignerViewSet)
router.register(r'trends', TrendViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('stats/', stats_view, name='stats'),
    
    # C'est ici que l'API devient accessible
    path('api/', include(router.urls)), 
]