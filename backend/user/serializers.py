from rest_framework import serializers
from user.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'email',
            'username',
            'password',
            'role',
            'title',
            'image_s3_path',
        )

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user


class UserBlockSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'is_blocked',
        )
