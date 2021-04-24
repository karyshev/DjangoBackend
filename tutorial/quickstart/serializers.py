from django.contrib.auth.models import User
from rest_framework import serializers
from tutorial.quickstart.models import Tweet, Follow


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'first_name', 'last_name', 'email']
        extra_kwargs = {'url': {'lookup_field': 'username'}}


class TweetSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)

    class Meta:
        model = Tweet
        fields = ['id', 'url', 'text', 'photo', 'created', 'author']


class FollowSerializer(serializers.ModelSerializer):
    class Meta:
        model = Follow
        fields = []


class UserFollowsSerializer(serializers.ModelSerializer):
    follows = UserSerializer()

    class Meta:
        model = Follow
        fields = ['follows', 'followed']


class UserFollowedSerializer(serializers.ModelSerializer):
    follower = UserSerializer()

    class Meta:
        model = Follow
        fields = ['follower', 'followed']

