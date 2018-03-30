from django.contrib.auth.models import User

from rest_framework import serializers

from .models import Tweet


class TweetSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = Tweet
        fields = ['id', 'user', 'tweet', 'date_published']


class UserSerializer(serializers.ModelSerializer):
    tweets = serializers.PrimaryKeyRelatedField(many=True, queryset=Tweet.objects.all())

    class Meta:
        model = User
        fields = ['id', 'username', 'tweets']
