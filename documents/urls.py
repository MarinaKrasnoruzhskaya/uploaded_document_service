from django.urls import path, include
from rest_framework.routers import SimpleRouter

from documents.apps import DocumentsConfig
from documents.views import DocumentViewSet, FileView

app_name = DocumentsConfig.name

router = SimpleRouter()
router.register(r"documents", DocumentViewSet)

urlpatterns = [
    path('media/documents/<str:document_url>/', FileView.as_view()),
]

urlpatterns += router.urls
