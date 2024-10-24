from django.urls import path

from documents.apps import DocumentsConfig
from documents.views import FileView, DocumentUploadView

app_name = DocumentsConfig.name

urlpatterns = [
    path('document/upload/', DocumentUploadView.as_view(), name='upload'),
    path('media/documents/<str:document>/', FileView.as_view()),
]
