from rest_framework import serializers
from innotter.models import Tag, Page, Post


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'


class PageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Page
        exclude = ('is_blocked', 'unblock_date', 'followers', 'follow_requests')


class PageRetrieveSerializer(serializers.ModelSerializer):
    class Meta:
        model = Page
        fields = ['name', 'uuid', 'description', 'tags', 'is_private']


class PageListSerializer(serializers.ModelSerializer):
    tags = serializers.StringRelatedField(many=True)
    owner = serializers.StringRelatedField()
    follow_requests = serializers.StringRelatedField(many=True)
    followers = serializers.StringRelatedField(many=True)

    class Meta:
        model = Page
        fields = '__all__'


class PostListSerializer(serializers.ModelSerializer):
    page = serializers.StringRelatedField()
    reply_to = serializers.StringRelatedField()

    class Meta:
        model = Post
        fields = '__all__'


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = '__all__'


class PagePermanentBlockSerializer(serializers.ModelSerializer):
    class Meta:
        model = Page
        fields = ['is_blocked']


class PageTemporaryBlockSerializer(serializers.ModelSerializer):
    class Meta:
        model = Page
        fields = ['unblock_date']


class FollowRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Page
        fields = ['follow_requests', ]
