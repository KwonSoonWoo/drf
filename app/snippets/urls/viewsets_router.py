from django.urls import include, path
from rest_framework.routers import DefaultRouter, SimpleRouter

from..views import viewsets as views

router = SimpleRouter()
router.register(r'snippets', views.SnippetViewSet)
router.register(r'users', views.UserViewSet)

urlpatterns = [
    path('', include(router.urls))
]
