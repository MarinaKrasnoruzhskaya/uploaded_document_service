from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from documents.models import Document
from documents.services import get_upload_file

from users.models import User


class DocumentUploadTestCase(APITestCase):
    """ Класс для тестирования загрузки документа """

    def setUp(self):
        self.user = User.objects.create(email='test_user@hht.com')
        self.client.force_authenticate(user=self.user)

    def test_document_upload_unauthorized(self):
        """ Тестирование загрузки документа неавторизованным пользователем"""

        self.client.force_authenticate(user=None)
        url = reverse("documents:upload")
        upload_file = get_upload_file('test_file.txt')
        data = {
            "document": upload_file,
        }
        response = self.client.post(url, data)
        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED
        )

    def test_document_upload(self):
        """ Тестирование загрузки документа авторизованным пользователем"""

        self.client.force_authenticate(user=self.user)
        url = reverse("documents:upload")
        upload_file = get_upload_file('test_file.txt')
        print(upload_file)
        data = {
            "document": upload_file,
        }
        response = self.client.post(url, data)
        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED
        )
        self.assertEqual(
            Document.objects.all().count(),
            1
        )

    def test_empty_document_upload(self):
        """ Тестирование загрузки пустого документа"""

        url = reverse("documents:upload")
        data = {
            "document": 'test_file.txt',
        }
        response = self.client.post(url, data)
        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST
        )
        self.assertEqual(
            Document.objects.all().count(),
            0
        )
