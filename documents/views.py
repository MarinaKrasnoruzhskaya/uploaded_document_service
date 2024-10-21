from django.shortcuts import render
from rest_framework.permissions import IsAdminUser
from rest_framework.viewsets import ModelViewSet

from documents.models import Document
from documents.serializers import DocumentSerializer

from documents.tasks import send_notification


class DocumentViewSet(ModelViewSet):
    """ Класс-представление для работы с документами """

    queryset = Document.objects.all()
    serializer_class = DocumentSerializer
    http_method_names = ['post', 'patch', 'get']

    def perform_create(self, serializer):
        """ Метод для автоматической привязки загруженного документа к авторизованному пользователю и
        определения задачи для отправки уведомления администратору """

        serializer.save(author=self.request.user)
        id_ = serializer.data['id']  # Получаем ID нового документа для отправки письма
        send_notification.delay(id_)

    def perform_update(self, serializer):
        """ Метод определяет задачу для отправки уведомления автору документа после проверки администратором """

        serializer.save()
        status_ = serializer.data['status']
        if status_ in ['document confirmed', 'document rejected']:
            id_ = serializer.data['id']
            send_notification.delay(id_)

    def get_permissions(self):
        """ Метод определяет доступ администратора к просмотру документа и изменению его статуса """

        if self.action in ["update", "retrieve", "partial_update"]:
            self.permission_classes = (IsAdminUser,)
        return super().get_permissions()
