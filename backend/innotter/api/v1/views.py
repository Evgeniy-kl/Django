from rest_framework import viewsets, mixins
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.exceptions import MethodNotAllowed
from django.db.models import Q
import datetime

from innotter.api.permissions import IsUser, IsAdmin, IsModerator, IsOwner
from innotter.models import Tag, Page, Post
from innotter.api.serializers import (
    PageSerializer,
    TagSerializer,
    PostSerializer,
    PageListSerializer,
    PagePermanentBlockSerializer,
    PageTemporaryBlockSerializer,
    PostListSerializer,
    FollowRequestSerializer,
)
from user.models import User


class TagViewSet(viewsets.GenericViewSet,
                 mixins.ListModelMixin,
                 mixins.CreateModelMixin,
                 mixins.UpdateModelMixin,
                 mixins.RetrieveModelMixin,
                 mixins.DestroyModelMixin):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class PageViewSet(mixins.ListModelMixin,
                  mixins.CreateModelMixin,
                  mixins.UpdateModelMixin,
                  mixins.RetrieveModelMixin,
                  mixins.DestroyModelMixin,
                  viewsets.GenericViewSet):
    serializers = {'list': PageListSerializer,
                   'retrieve': PageListSerializer,
                   'create': PageSerializer,
                   'permanent_blocking': PagePermanentBlockSerializer,
                   'temporary_blocking': PageTemporaryBlockSerializer,
                   'follow_requests': FollowRequestSerializer}
    queryset = Page.objects.prefetch_related(
        'tags',
        'followers',
        'follow_requests',
    ).select_related(
        'owner'
    ).filter(
        Q(is_blocked=False),
        Q(
            Q(unblock_date__lte=datetime.datetime.now()) |
            Q(unblock_date=None)
        )
    ).all()
    serializer_class = PageSerializer
    permission_classes = (IsAuthenticated,)

    def get_serializer_class(self):
        return self.serializers.get(self.action, self.serializer_class)

    def get_permissions(self):
        if self.action in ['permanent_blocking', 'destroy']:
            self.permission_classes = [IsAdmin, ]
        if self.action in ['temporary_blocking', ]:
            self.permission_classes = [IsModerator, IsAdmin]

        return super(self.__class__, self).get_permissions()

    @action(methods=['POST', 'GET'], detail=True)
    def permanent_blocking(self, request, **kwargs):
        return super().partial_update(request, **kwargs)

    @action(methods=['POST', 'GET'], detail=True)
    def temporary_blocking(self, request, **kwargs):
        return super().partial_update(request, **kwargs)

    @action(methods=['POST', 'GET'], detail=True)
    def follow_requests_decline_all(self, request, pk=None):
        page = Page.objects.get(pk=pk)
        user = User.objects.get(email=request.user.email)
        if page.owner == user:
            page.follow_requests.clear()
            page.save()
            return Response({'Decline all follow requests'})
        else:
            return Response({'Smth wrong'})

    @action(methods=['POST', 'GET'], detail=True)
    def follow_requests_accept_all(self, request, pk=None):
        user = User.objects.get(email=request.user.email)
        page = Page.objects.get(pk=pk)
        if page.owner == user:
            for follow_req in page.follow_requests.all():
                page.followers.add(follow_req)
                page.follow_requests.remove(follow_req)
            page.save()
            return Response({'Accept all follow requests'})
        else:
            return Response({'Smth wrong'})

    @action(methods=['GET'], detail=True)
    def follow(self, request, pk=None):
        page = Page.objects.get(pk=pk)
        user = User.objects.get(email=request.user.email)
        if page.is_private:
            page.follow_requests.add(user)
            page.save()
            return Response({'Follow request sent'})
        else:
            page.followers.add(user)
            page.save()
            return Response({'Followed'})

    @action(methods=['GET'], detail=True)
    def unfollow(self, request, pk=None):
        page = Page.objects.get(pk=pk)
        user = User.objects.get(email=request.user.email)
        try:
            page.follow_requests.remove(user)
            page.followers.remove(user)
            page.save()
        except MethodNotAllowed:
            return Response({'Smth wrong'})

        return Response({'Unfollowed'})


class PostViewSet(viewsets.GenericViewSet,
                  mixins.ListModelMixin,
                  mixins.CreateModelMixin,
                  mixins.UpdateModelMixin,
                  mixins.RetrieveModelMixin,
                  mixins.DestroyModelMixin):
    queryset = Post.objects.select_related(
        'page',
        'reply_to',
    ).all()
    serializers = {'list': PostListSerializer,
                   'retrieve': PostListSerializer, }
    serializer_class = PostSerializer

    def get_serializer_class(self):
        return self.serializers.get(self.action, self.serializer_class)

    def get_permissions(self):
        if self.action in ['destroy']:
            self.permission_classes = [IsAdmin, IsModerator]

        return super(self.__class__, self).get_permissions()

    @action(methods=['POST', 'GET'], detail=True)
    def like(self, request, pk=None):
        post = Post.objects.get(pk=pk)
        user = User.objects.get(email=request.user.email)
        post.is_liked.add(user)
        post.save()
        return Response({'Liked'})

    @action(methods=['POST', 'GET'], detail=True)
    def unlike(self, request, pk=None):
        post = Post.objects.get(pk=pk)
        user = User.objects.get(email=request.user.email)
        post.is_liked.remove(user)
        post.save()
        return Response({'Unliked'})
