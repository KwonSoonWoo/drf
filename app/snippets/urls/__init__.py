from django.urls import path, include

# /snippets/snippets/
# /snippets/snippets/<pk>/

# /snippets/django_view/snippets/
# /snippets/django_view/snippets/<pk>

from . import django_view

app_name = 'snippets'
urlpatterns = [
    # config.urls를 참조
    path('django_view/', include(django_view)),
]