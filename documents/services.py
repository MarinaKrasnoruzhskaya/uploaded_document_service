import io
import os

import magic
from django.core.files.uploadedfile import InMemoryUploadedFile

from config.settings import BASE_DIR


def get_upload_file(name):
    """ Функция для создания загружаемого файла """

    document_path = os.path.join(BASE_DIR, "documents", "data", name)
    byte_io = io.BytesIO()
    with open(document_path, 'rb') as file:
        byte_io.write(file.read())
        byte_io.seek(0)

    mime = magic.Magic(mime=True)
    content_type = mime.from_file(document_path)

    return InMemoryUploadedFile(
        file=byte_io,
        field_name='document',
        name=name,
        content_type=content_type,
        size=os.path.getsize(document_path),
        charset=None
    )
