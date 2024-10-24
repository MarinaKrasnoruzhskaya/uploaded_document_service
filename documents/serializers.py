from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from documents.models import Document


class DocumentUploadSerializer(ModelSerializer):
    """ Класс-сериализатор для загрузки документа """

    document = serializers.FileField(required=True)

    class Meta:
        model = Document
        fields = ('document',)


class FileViewSerializer(ModelSerializer):
    """ Класс-сериализатор для отображения загруженного файла """

    document = serializers.FileField(read_only=True)  # Отображаем только поле с файлом

    class Meta:
        model = Document
        fields = ('document',)
