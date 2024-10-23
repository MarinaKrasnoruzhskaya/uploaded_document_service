from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from documents.models import Document


class DocumentSerializer(ModelSerializer):
    """ Класс-сериализатор для модели Документ """
    class Meta:
        model = Document
        fields = "__all__"


class FileViewSerializer(ModelSerializer):
    """ Класс-сериализатор для отображения загруженного файла """
    document_url = serializers.FileField(read_only=True)  # Отображаем только поле с файлом

    class Meta:
        model = Document
        fields = ('document_url',)
