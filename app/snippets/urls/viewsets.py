from django.urls import path

from ..views.viewsets import (
    SnippetViewSet,
    UserViewSet,
)


snippet_list = SnippetViewSet.as_view({
    'get': 'list',
    'post': 'create',
})
snippet_detail = SnippetViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy',
})

user_list = UserViewSet.as_view({
    'get': 'list',
})
user_detail = UserViewSet.as_view({
    'get': 'retrieve',
})

urlpatterns = [
    path('snippets/',
         snippet_list,
         name='snippet-list'),
    path('snippets/<int:pk>/',
         snippet_detail,
         name='snippet-detail'),
    path('users/',
         user_list,
         name='user-list'),
    path('users/<int:pk>/',
         user_detail,
         name='user-detail'),
]