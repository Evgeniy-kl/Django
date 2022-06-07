from rest_framework import viewsets, mixins
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from innotter.tasks import send_mail_to
from innotter.models import Tag, Page, Post
from innotter.serializers import (
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

    # permission_classes = (IsAuthenticated,)

    def get_serializer_class(self):
        return self.serializers.get(self.action, self.serializer_class)

    @action(methods=('PATCH',), detail=True)
    def permanent_block(self, request, **kwargs):
        return super().partial_update(request, **kwargs)

    @action(methods=('PATCH',), detail=True)
    def temporary_block(self, request, **kwargs):
        return super().partial_update(request, **kwargs)

    @action(methods=('POST',), detail=True)
    def follow_requests_decline_all(self, request, pk=None):
        FollowService.decline_all_followers(self.get_object(), request.user)
        return Response('Decline all follow requests')

    @action(methods=('POST',), detail=True)
    def follow_requests_accept_all(self, request, pk=None):
        FollowService.decline_all_followers(self.get_object(), request.user)
        return Response('Accept all follow requests')

    @action(methods=('POST',), detail=True)
    def follow(self, request, pk=None):
        FollowService.follow(self.get_object(), request.user)
        return Response('Followed')

    @action(methods=('POST',), detail=True)
    def unfollow(self, request, pk=None):
        FollowService.unfollow(self.get_object(), request.user)
        return Response('Unfollowed')

    @action(methods=('GET',), detail=False)
    def my_pages(self, request):
        pages = FollowService.my_pages(request.user)
        return Response(pages)


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

    def perform_create(self, serializer):
        serializer.save()
        FollowService.notification_to_subscribers(serializer.data['page'])

    @action(methods=('POST',), detail=True)
    def like(self, request, pk=None):
        LikeService.like(self.get_object(), request.user)
        return Response('Liked')

    @action(methods=('POST',), detail=True)
    def unlike(self, request, pk=None):
        LikeService.unlike(self.get_object(), request.user)
        return Response('Unliked')
