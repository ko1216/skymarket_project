from rest_framework import serializers

from ads.models import Comment, Ad


# Сериалайзеры

class CommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comment
        fields = ('ad', 'author', 'created_at', 'text',)


class AdSerializer(serializers.ModelSerializer):

    class Meta:
        model = Ad
        fields = ('title', 'image', 'price', 'description', 'created_at', 'author',)


class AdDetailSerializer(serializers.ModelSerializer):
    # сериалайзер для модели
    pass
