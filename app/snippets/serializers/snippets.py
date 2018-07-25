from django.contrib.auth import get_user_model
from rest_framework import serializers

from .users import UserListSerializer
from ..models import Snippet

User = get_user_model()

__all__ = (
    'SnippetListSerializer',
    'SnippetDetailSerializer',
)


class SnippetBaseSerializer(serializers.ModelSerializer):
    owner = UserListSerializer(required=False)

    class Meta:
        model = Snippet
        fields = (
            'pk',
            'title',
            'linenos',
            'language',
            'style',
            'owner',
        )
        read_only_fields = (
            'owner',
        )


class SnippetListSerializer(SnippetBaseSerializer):
    pass


class SnippetDetailSerializer(SnippetBaseSerializer):
    class Meta(SnippetBaseSerializer.Meta):
        fields = SnippetBaseSerializer.Meta.fields + ('code',)



