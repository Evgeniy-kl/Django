from rest_framework import serializers
from innotter.models import Tag, Page, Post
from innotter.services import ValidateFileFormat


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = (
            'name',
        )


class PageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Page
        exclude = (
            'is_blocked',
            'unblock_date',
            'followers',
            'follow_requests',
        )

    def create(self, validated_data):
        image = validated_data.pop('image')
        tags = validated_data.pop('tags')
        if not ValidateFileFormat.is_valid_file(image):
            raise serializers.ValidationError("Not Valid file format!")
        page = Page(**validated_data)
        page.image = image
        page.save()
        return page


class PageRetrieveSerializer(serializers.ModelSerializer):
    class Meta:
        model = Page
        fields = (
            'name',
            'uuid',
            'description',
            'tags',
            'is_private',
        )


class PageListSerializer(serializers.ModelSerializer):
    tags = serializers.StringRelatedField(many=True)
    owner = serializers.StringRelatedField()
    follow_requests = serializers.StringRelatedField(many=True)
    followers = serializers.StringRelatedField(many=True)

    class Meta:
        model = Page
        fields = (
            'name',
            'uuid',
            'description',
            'tags',
            'owner',
            'followers',
            'image',
            'is_private',
            'follow_requests',
            'is_blocked',
            'unblock_date',
        )


class PostListSerializer(serializers.ModelSerializer):
    page = serializers.StringRelatedField()
    reply_to = serializers.StringRelatedField()

    class Meta:
        model = Post
        fields = (
            'id',
            'page',
            'content',
            'reply_to',
            'liked_by',
        )


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = (
            'page',
            'content',
            'reply_to',
            'liked_by',
        )


class PagePermanentBlockSerializer(serializers.ModelSerializer):
    class Meta:
        model = Page
        fields = (
            'is_blocked',
        )


class PageTemporaryBlockSerializer(serializers.ModelSerializer):
    class Meta:
        model = Page
        fields = (
            'unblock_date',
        )


class FollowRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Page
        fields = (
            'follow_requests',
        )
