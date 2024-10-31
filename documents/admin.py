import admin_confirm
from django.contrib import admin
from django.db import transaction

from documents.models import Document
from documents.tasks import send_notification


@admin.register(Document)
class DocumentAdmin(admin_confirm.AdminConfirmMixin, admin.ModelAdmin):
    list_display = (
        "id",
        "document",
        "author",
        "created_at",
        "status",
    )
    confirm_change = True
    confirmation_fields = ['status',]
    list_editable = ('status',)
    actions = ["make_published", "make_rejected"]

    @admin.action(description="Подтвердить выбранные документы")
    def make_published(self, request, queryset):
        """ Для выбранных документов изменение статуса на 'документ подтвержден' и отображение этого действия
        в списке действий """

        queryset.update(status="document confirmed")
        for document in queryset:
            send_notification.delay(document.pk)

    @admin.action(description="Отклонить выбранные документы")
    def make_rejected(self, request, queryset):
        """ Для выбранных документов изменение статуса на 'документ отклонен' и отображение этого действия
        в списке действий """

        queryset.update(status="document rejected")
        for document in queryset:
            send_notification.delay(document.pk)

    @transaction.atomic
    def save_model(self, request, obj, form, change):
        """ Метод определяет задачу для отправки уведомления автору документа после проверки администратором """

        if change:
            old_status: str = Document.objects.get(pk=obj.pk).status
            new_status: str = form.cleaned_data['status']
            if old_status != new_status:
                send_notification.delay(obj.id)
        super().save_model(request, obj, form, change)
