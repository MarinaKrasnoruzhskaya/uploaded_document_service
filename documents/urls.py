from django.urls import path, include
from rest_framework.routers import SimpleRouter

from documents.apps import DocumentsConfig
from documents.views import DocumentViewSet

app_name = DocumentsConfig.name

router = SimpleRouter()
router.register(r"documents", DocumentViewSet)

urlpatterns = [
    path('', include(router.urls))
]
