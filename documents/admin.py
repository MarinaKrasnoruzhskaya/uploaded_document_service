from django.contrib import admin
from django.db import transaction

from documents.models import Document
from documents.tasks import send_notification


@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "document_url",
        "author",
        "created_at",
        "status",
    )

    @transaction.atomic
    def save_model(self, request, obj, form, change):
        """ Метод определяет задачу для отправки уведомления автору документа после проверки администратором """

        if change:
            old_status = Document.objects.get(pk=obj.pk).status
            new_status = form.cleaned_data['status']

        super().save_model(request, obj, form, change)

        if old_status != new_status:
            send_notification.delay(obj.id)
