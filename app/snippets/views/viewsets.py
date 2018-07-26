from django.contrib.auth import get_user_model
from rest_framework import viewsets, permissions

from ..models import Snippet
from ..permissions import IsOwnerOrReadOnly
from ..serializers import UserListSerializer, SnippetListSerializer

User = get_user_model()


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserListSerializer


class SnippetViewSet(viewsets.ModelViewSet):
    queryset = Snippet.objects.all()
    serializer_class = SnippetListSerializer
    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly,
        IsOwnerOrReadOnly,
    )

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)