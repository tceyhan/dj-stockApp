from django.urls import path
from .views import (
    CategoryView,
    BrandView,
    ProductView,
)

from rest_framework import routers
router = routers.DefaultRouter()
router.register("category", CategoryView)
router.register("brand", BrandView)
router.register("product", ProductView)

urlpatterns = [
    
] + router.urls
