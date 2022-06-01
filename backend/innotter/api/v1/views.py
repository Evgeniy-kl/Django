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
from innotter.services import FollowService, LikeService


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
                  viewsets.GenericViewSet, ):
    serializers = {'list': PageListSerializer,
                   'retrieve': PageListSerializer,
                   'create': PageSerializer,
                   'permanent_block': PagePermanentBlockSerializer,
                   'temporary_block': PageTemporaryBlockSerializer,
                   'follow_requests': FollowRequestSerializer}
    queryset = Page.active_pages.prefetch_related(
        'tags',
        'followers',
        'follow_requests',
    ).select_related(
        'owner'
    ).all()
    serializer_class = PageSerializer
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        return self.serializers.get(self.action, self.serializer_class)

    @action(methods=['PATCH'], detail=True)
    def permanent_block(self, request, **kwargs):
        return super().partial_update(request, **kwargs)

    @action(methods=['PATCH'], detail=True)
    def temporary_block(self, request, **kwargs):
        return super().partial_update(request, **kwargs)

    @action(methods=['POST'], detail=True)
    def follow_requests_decline_all(self, request, pk=None):
        initiate_follow_service = FollowService()
        try:
            initiate_follow_service.decline_all_followers(self.get_object(), request.user)
            return Response('Decline all follow requests')
        except MethodNotAllowed:
            return Response('Smth wrong')

    @action(methods=['POST'], detail=True)
    def follow_requests_accept_all(self, request, pk=None):
        initiate_follow_service = FollowService()
        try:
            initiate_follow_service.decline_all_followers(self.get_object(), request.user)
            return Response('Accept all follow requests')
        except MethodNotAllowed:
            return Response('Smth wrong')

    @action(methods=['POST'], detail=True)
    def follow(self, request, pk=None):
        initiate_follow_service = FollowService()
        try:
            initiate_follow_service.follow(self.get_object(), request.user)
            return Response('Followed')
        except MethodNotAllowed:
            return Response('Smth wrong')

    @action(methods=['POST'], detail=True)
    def unfollow(self, request, pk=None):
        initiate_follow_service = FollowService()
        try:
            initiate_follow_service.unfollow(self.get_object(), request.user)
            return Response('Unfollowed')
        except MethodNotAllowed:
            return Response('Smth wrong')

    @action(methods=['GET'], detail=False)
    def my_pages(self, request):
        initiate_follow_service = FollowService()
        try:
            pages = initiate_follow_service.my_pages(request.user)
            return Response(pages)
        except MethodNotAllowed:
            return Response('Smth wrong')


class PostViewSet(viewsets.GenericViewSet,
                  mixins.ListModelMixin,
                  mixins.CreateModelMixin,
                  mixins.UpdateModelMixin,
                  mixins.RetrieveModelMixin,
                  mixins.DestroyModelMixin, ):
    queryset = Post.objects.select_related(
        'page',
        'reply_to',
    ).all()
    serializers = {'list': PostListSerializer,
                   'retrieve': PostListSerializer, }
    serializer_class = PostSerializer

    def get_serializer_class(self):
        return self.serializers.get(self.action, self.serializer_class)

    @action(methods=['POST'], detail=True)
    def like(self, request, pk=None):
        initiate_like_service = LikeService()
        try:
            initiate_like_service.like(self.get_object(), request.user)
            return Response('Liked')
        except MethodNotAllowed:
            return Response('Smth wrong')

    @action(methods=['POST'], detail=True)
    def unlike(self, request, pk=None):
        initiate_like_service = LikeService()
        try:
            initiate_like_service.unlike(self.get_object(), request.user)
            return Response('Unliked')
        except MethodNotAllowed:
            return Response('Smth wrong')
