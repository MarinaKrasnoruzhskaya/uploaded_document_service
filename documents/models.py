from django.db import models

from config.settings import AUTH_USER_MODEL


class Document(models.Model):
    """ Класс для модели Document """

    STATUSES = (
        ('document uploaded', 'документ загружен'),
        ('document confirmed', 'документ подтвержден'),
        ('document rejected', 'документ отклонен'),
    )

    document = models.FileField(upload_to='documents', verbose_name='загруженный документ')
    author = models.ForeignKey(
        AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name='автор документа',
        blank=True,
        null=True
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='дата и время загрузки')
    status = models.CharField(
        max_length=20,
        choices=STATUSES,
        default='document uploaded',
        verbose_name='статус документа'
    )

    def __str__(self):
        return f"{self.author}: {self.document}"

    class Meta:
        verbose_name = "документ"
        verbose_name_plural = "документы"
