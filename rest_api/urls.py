from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from django.conf.urls import include
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register(r'swarms', views.SwarmViewSet)
router.register(r'nodes', views.NodeViewSet)
router.register(r'services', views.ServiceViewSet)
router.register(r'deployments', views.DeploymentViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
