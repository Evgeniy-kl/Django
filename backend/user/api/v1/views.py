from rest_framework import viewsets, mixins
from rest_framework.decorators import action

from user.models import User
from user.api.serializers import UserSerializer, UserBlockSerializer


class UserViewSet(viewsets.GenericViewSet,
                  mixins.CreateModelMixin,
                  mixins.RetrieveModelMixin,
                  mixins.UpdateModelMixin,
                  mixins.ListModelMixin):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    serializers = {'blocking': UserBlockSerializer}

    def get_serializer_class(self):
        return self.serializers.get(self.action, self.serializer_class)

    @action(methods=['POST', 'GET'], detail=True)
    def blocking(self, request, **kwargs):
        return super().partial_update(request, **kwargs)
