from rest_framework import viewsets, mixins
from rest_framework.decorators import action
from rest_framework.exceptions import MethodNotAllowed
from rest_framework.response import Response

from user.models import User
from user.api.serializers import UserSerializer, UserBlockSerializer
from user.services import UserService

class UserViewSet(viewsets.GenericViewSet,
                  mixins.CreateModelMixin,
                  mixins.RetrieveModelMixin,
                  mixins.UpdateModelMixin,
                  mixins.ListModelMixin):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    serializers = {'block': UserBlockSerializer}

    def get_serializer_class(self):
        return self.serializers.get(self.action, self.serializer_class)

    @action(methods=['PATCH'], detail=True)
    def block(self, request, **kwargs):
        return super().partial_update(request, **kwargs)

    @action(methods=['GET'], detail=False)
    def liked_posts(self, request):
        initiate_user_service = UserService()
        try:
            posts = initiate_user_service.show_liked_posts(request.user)
            return Response(posts)
        except MethodNotAllowed:
            return Response('Smth wrong')




