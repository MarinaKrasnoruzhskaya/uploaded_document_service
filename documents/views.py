from rest_framework import mixins
from rest_framework.viewsets import ModelViewSet

from documents.models import Document
from documents.serializers import DocumentSerializer

from documents.tasks import send_notification


class DocumentViewSet(ModelViewSet):
    """ Класс-представление для работы с документами """

    queryset = Document.objects.all()
    serializer_class = DocumentSerializer
    http_method_names = ['post']

    def perform_create(self, serializer):
        """ Метод для автоматической привязки загруженного документа к авторизованному пользователю и
        для определения задачи отправки уведомления администратору """

        serializer.save(author=self.request.user)
        id_ = serializer.data['id']  # Получаем ID нового документа для отправки письма
        send_notification.delay(id_)
