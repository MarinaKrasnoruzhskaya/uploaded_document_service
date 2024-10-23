from django.http.response import FileResponse
from rest_framework.generics import get_object_or_404
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from documents.models import Document
from documents.serializers import DocumentSerializer, FileViewSerializer

from documents.tasks import send_notification


class DocumentViewSet(ModelViewSet):
    """ Класс-представление для работы с документами """

    queryset = Document.objects.all()
    serializer_class = DocumentSerializer
    http_method_names = ['post', 'get']
    parser_classes = [MultiPartParser, FormParser]

    def perform_create(self, serializer):
        """ Метод для автоматической привязки загруженного документа к авторизованному пользователю и
        для определения задачи отправки уведомления администратору """

        serializer.save(author=self.request.user)
        id_ = serializer.data['id']  # Получаем ID нового документа для отправки письма
        send_notification.delay(id_)


class FileView(APIView):
    """ Класс-представление для отображения загруженного файла """
    queryset = Document.objects.all()
    serializer_class = FileViewSerializer
    permission_classes = [AllowAny,]
    parser_classes = [MultiPartParser, FormParser]

    def get(self, request, document_url):
        """ Метод для получения файла по его url и отправки его в виде скачиваемого файла """

        document = get_object_or_404(Document, document_url=f"documents/{document_url}")
        return FileResponse(document.document_url, as_attachment=True)
