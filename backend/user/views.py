from rest_framework import viewsets, mixins
from rest_framework.decorators import action
from rest_framework.response import Response

from user.models import User
from user.serializers import UserSerializer, UserBlockSerializer
from user.services import UserService, BlockService


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

    @action(methods=('PATCH',), detail=True)
    def block(self, request, **kwargs):
        BlockService.block_all_pages(self.get_object(), request)
        return super().partial_update(request, **kwargs)

    @action(methods=('GET',), detail=False)
    def liked_posts(self, request):
        posts = UserService.show_liked_posts(request.user)
        return Response(posts)

    @action(methods=('GET',), detail=False)
    def dashboard(self, request):
        result = UserService.dashboard(user=request.user)
        return Response(result)
