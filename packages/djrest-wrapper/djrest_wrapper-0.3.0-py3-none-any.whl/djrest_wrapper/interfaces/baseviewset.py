from rest_framework.viewsets import GenericViewSet
from ..paginations import DefaultPagination
from .mixins import CreateMixin, RetrieveMixin, UpdateMixin, ListMixin, DestroyMixin
from ..exceptions.apis import AuthenticationFailedExp, PemissionDeniedExp

class BaseViewSet(GenericViewSet, CreateMixin, RetrieveMixin, UpdateMixin, ListMixin, DestroyMixin):
    serializer_action_classes = {}
    permission_action_classes = {}
    page_size = 10
    pagination_class = DefaultPagination

    def get_serializer_class(self, *args, **kwargs):
        try:
            if self.action == 'list':
                return self.serializer_action_classes.get(self.action).get('res')
            return self.serializer_action_classes.get(self.action).get(kwargs.get('type', 'req'))
        except:
            return super().get_serializer_class()

    def get_serializer_response(self):
        return self.get_serializer_class(type='res')

    def get_permissions(self):
        try:
            return [permission() for permission in self.permission_action_classes[self.action]]
        except:
            return super().get_permissions()

    @property
    def paginator(self):
        if not hasattr(self, '_paginator'):
            if self.pagination_class is None:
                self._paginator = None
            else:
                self._paginator = self.pagination_class()
                self._paginator.page_size = self.page_size
                self._paginator.page_result_key = self.queryset.model._meta.verbose_name_plural
        return self._paginator

    def get_queryset(self):
        if self.action == 'list':
            qs = self.queryset.all()
            return qs
        else:
            return super().get_queryset()

    def permission_denied(self, request, message=None, code=None):
        if request.authenticators and not request.successful_authenticator:
            raise AuthenticationFailedExp('Unauthenticated')
        raise PemissionDeniedExp('Permission Denied')

