# polls/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PollViewSet, OptionViewSet, VoteViewSet, api_root

router = DefaultRouter()
router.register(r"polls", PollViewSet, basename="poll")
router.register(r"options", OptionViewSet, basename="option")
router.register(r"votes", VoteViewSet, basename="vote")

urlpatterns = [
    path("", api_root, name="api-root"),
    path("", include(router.urls)),
]
