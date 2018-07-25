from django.contrib.auth import get_user_model
from rest_framework import serializers
from .models import LANGUAGE_CHOICES, STYLE_CHOICES, Snippet

User = get_user_model()

__all__ = (
    'UserSerializer',
    'SnippetSerializer',
)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'pk',
            'username',
            'snippets',
        )


class SnippetSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    class Meta:
        model = Snippet
        fields = (
            'pk',
            'title',
            'code',
            'linenos',
            'language',
            'style',
            'style',
            'owner',
        )
        # 읽기 전용.
        read_only_fields = (
            'owner',
        )