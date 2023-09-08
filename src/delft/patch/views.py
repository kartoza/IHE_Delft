import logging
# Standard Modules
import os

# Django functionality
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.template import loader
from django.utils.text import slugify
from django.utils.translation import ugettext as _
from django_downloadview.response import DownloadResponse
from geonode.base import register_event
# Geonode functionality
from geonode.documents.models import Document
from geonode.monitoring.models import EventType
from geonode.storage.data_retriever import DataItemRetriever
from geonode.storage.manager import storage_manager

logger = logging.getLogger(__name__)


def open(name, mode='rb'):
    try:
        return storage_manager._concrete_storage_manager.open(name, mode=mode)
    except Exception as e:
        print(f'6 - error {e}')
        files_path = DataItemRetriever(_file=name).transfer_remote_file()
        print(f'6 - error {files_path}')
        return storage_manager._concrete_storage_manager.open(
            files_path, mode=mode
        )


def get_download_response(request, docid, attachment=False):
    """
    Returns a download response if user has access to download the document of a given id,
    and an http response if they have no permissions to download it.
    """
    document = get_object_or_404(Document, pk=docid)
    print(f'Download response')
    print(f'1 - {document.id}')
    logger.debug(f'1 - {document.id}')

    if not request.user.has_perm(
            'base.download_resourcebase',
            obj=document.get_self_resource()):
        print(f'2 - Does not have permission')
        logger.debug(f'2 - Does not have permission')
        return HttpResponse(
            loader.render_to_string(
                '401.html', context={
                    'error_message': _(
                        "You are not allowed to view this document.")},
                request=request), status=401)
    print(f'3 - {attachment}')
    logger.debug(f'3 - {attachment}')
    if attachment:
        register_event(request, EventType.EVENT_DOWNLOAD, document)
    filename = slugify(os.path.splitext(os.path.basename(document.title))[0])
    print(f'4 - {filename}')
    logger.debug(f'4 - {filename}')
    print(f'5 - {document.files}')
    logger.debug(f'5 - {document.files}')
    print(f'6 - {storage_manager.exists(document.files[0])}')
    logger.debug(f'6 - {storage_manager.exists(document.files[0])}')

    if document.files and storage_manager.exists(document.files[0]):
        _file = open(document.files[0])
        print(f'7 - {_file}')
        logger.debug(f'7 - {_file}')
        print(f'8 - {_file.size}')
        logger.debug(f'8 - {_file.size}')
        print(f'9 - {filename}.{document.extension}')
        logger.debug(f'9 - {filename}.{document.extension}')
        print(f'10 - {request.headers}')
        logger.debug(f'10 - {request}')
        response = DownloadResponse(
            _file.file,
            basename=f'{filename}.{document.extension}',
            attachment=attachment
        )
        print(f'11 - {response.headers}')
        logger.debug(response.headers)
        return response
    return HttpResponse(
        "File is not available",
        status=404
    )


def document_download(request, docid):
    response = get_download_response(request, docid, attachment=True)
    return response


def document_link(request, docid):
    response = get_download_response(request, docid)
    return response
