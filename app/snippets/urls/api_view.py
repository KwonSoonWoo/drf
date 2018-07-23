from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from ..views import api_view as views


urlpatterns = [
    path('snippets/',
         views.SnippetList.as_view(),
         name='snippet-list'),
    path('snippets/<int:pk>/',
         views.SnippetDetail.as_view(),
         name='snippet-detail'),
]

urlpatterns = format_suffix_patterns(urlpatterns)