from celery import shared_task
from django.core.mail import send_mail

from config import settings
from documents.models import Document
from users.models import User


@shared_task
def send_notification(pk: int):
    """ Отправка уведомлений """

    document = Document.objects.get(pk=pk)

    if document.status == 'document uploaded':
        admin = User.objects.get(is_superuser=True)
        send_mail(
            subject=f"Загружен новый документ!",
            message=f"Пользователем {document.author} загружен новый документ {document.document_url}",
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[admin.email],
            fail_silently=False,
        )
    else:
        send_mail(
            subject=f"Изменение статуса документа!",
            message=f"Статус документа {document} изменен на {document.status}",
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[document.author.email],
            fail_silently=False,
        )
