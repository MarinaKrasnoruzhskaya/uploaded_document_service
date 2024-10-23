from django.conf.urls.static import static
from django.urls import path

from config import settings
from documents.apps import DocumentsConfig
from documents.views import FileView, DocumentUploadView

app_name = DocumentsConfig.name

urlpatterns = [
    path('document/upload/', DocumentUploadView.as_view(), name='upload'),
    path('media/documents/<str:document_url>/', FileView.as_view()),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
