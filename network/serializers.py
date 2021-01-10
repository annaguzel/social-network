
from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Post


class UserCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'password', 'first_name', 'last_name']

    def create(self, validated_data):
        username = validated_data['username']
        password = validated_data['password']
        firstname = validated_data['first_name']
        lastname = validated_data['last_name']
        new_user = User(username=username,
                        first_name=firstname, last_name=lastname)
        new_user.set_password(password)
        new_user.save()
        return validated_data


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["username"]


class PostSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        validated_data['text'] = validated_data['text']
        return super().create(validated_data)

    class Meta:
        model = Post
        fields = (
            'id', 'text', 'user', 'created_at', 'likes'
        )
        read_only_fields = (
            'user', 'created_at',
        )
