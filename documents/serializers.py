from rest_framework.serializers import ModelSerializer

from documents.models import Document


class DocumentSerializer(ModelSerializer):
    """ Класс-сериализатор для модели Документ """
    class Meta:
        model = Document
        fields = "__all__"
