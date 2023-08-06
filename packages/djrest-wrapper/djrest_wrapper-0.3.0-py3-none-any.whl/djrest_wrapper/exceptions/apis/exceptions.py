from .base import BaseApiExp
from .errors import *
from rest_framework.status import *


class AuthenticationFailedExp(BaseApiExp):
    err_code = ERR_AUTHENTICATION_FAILED
    status_code = HTTP_401_UNAUTHORIZED


class DoesNotExistsExp(BaseApiExp):
    err_code = ERR_DOT_NOT_EXIST
    status_code = HTTP_404_NOT_FOUND


class DuplicateModelExp(BaseApiExp):
    err_code = ERR_DUPLICATE_MODEL
    status_code = HTTP_400_BAD_REQUEST


class MethodNotAllowedExp(BaseApiExp):
    err_code = ERR_METHOD_NOT_ALLOWED
    status_code = HTTP_405_METHOD_NOT_ALLOWED


class NotAcceptableExp(BaseApiExp):
    err_code = ERR_NOT_ACCEPTABLE
    status_code = HTTP_406_NOT_ACCEPTABLE


class UnauthenticatedExp(BaseApiExp):
    err_code = ERR_NOT_AUTHENTICATED
    status_code = HTTP_401_UNAUTHORIZED


class ParseErrorExp(BaseApiExp):
    err_code = ERR_PARSE
    status_code = HTTP_400_BAD_REQUEST


class PemissionDeniedExp(BaseApiExp):
    err_code = ERR_PERMISSION_DENIED
    status_code = HTTP_403_FORBIDDEN


class UnsupportedMediaExp(BaseApiExp):
    err_code = ERR_UNSUPPORTED_MEDIA
    status_code = HTTP_415_UNSUPPORTED_MEDIA_TYPE


class ValidationErrorExp(BaseApiExp):
    err_code = ERR_INPUT_VALIDATION
    status_code = HTTP_400_BAD_REQUEST


class ConflictErrorExp(BaseApiExp):
    err_code = ERR_CONFLICT
    status_code = HTTP_409_CONFLICT


class InternalError(BaseApiExp):
    err_code = ERR_INTERNAL
    status_code = HTTP_500_INTERNAL_SERVER_ERROR
