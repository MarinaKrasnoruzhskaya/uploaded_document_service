from django.http.response import FileResponse
from rest_framework import status
from rest_framework.generics import get_object_or_404
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from documents.models import Document
from documents.serializers import FileViewSerializer, DocumentUploadSerializer

from documents.tasks import send_notification


class DocumentUploadView(APIView):
    """ Класс-представление для загрузки документа """

    serializer_class = DocumentUploadSerializer
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request):
        document_serializer = DocumentUploadSerializer(data=request.data)
        if document_serializer.is_valid():
            document = document_serializer.save()
            document.author = request.user
            document.save()
            send_notification.delay(document.id)  # Отправка письма администратору
            return Response(document_serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(document_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class FileView(APIView):
    """ Класс-представление для отображения загруженного файла """
    queryset = Document.objects.all()
    serializer_class = FileViewSerializer
    permission_classes = [AllowAny,]
    parser_classes = [MultiPartParser, FormParser]

    def get(self, request, document):
        """ Метод для получения файла по его url и отправки его в виде скачиваемого файла """

        document_obj = get_object_or_404(Document, document=f"documents/{document}")
        print(document)
        return FileResponse(document_obj.document, as_attachment=True)
