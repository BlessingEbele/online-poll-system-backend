"""from rest_framework.routers import DefaultRouter
from .views import PollViewSet, OptionViewSet, VoteViewSet
from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

router = DefaultRouter()
router.register(r'polls', PollViewSet, basename='poll')
router.register(r'options', OptionViewSet, basename='option')
router.register(r'votes', VoteViewSet, basename='vote')

urlpatterns = router.urls


urlpatterns = [
    path('polls/', views.PollListCreateAPIView.as_view(), name='poll-list'),
    path('polls/<int:pk>/', views.PollRetrieveUpdateDestroyAPIView.as_view(), name='poll-detail'),
    path('options/', views.OptionListCreateAPIView.as_view(), name='option-list'),
    path('options/<int:pk>/', views.OptionRetrieveUpdateDestroyAPIView.as_view(), name='option-detail'),
    path('votes/', views.VoteListCreateAPIView.as_view(), name='vote-list'),
    path('votes/<int:pk>/', views.VoteRetrieveUpdateDestroyAPIView.as_view(), name='vote-detail'),
]

urlpatterns = format_suffix_patterns(urlpatterns)
"""

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'polls', views.PollViewSet, basename='poll')
router.register(r'options', views.OptionViewSet, basename='option')
router.register(r'votes', views.VoteViewSet, basename='vote')

urlpatterns = [
    path('', views.api_root, name='api-root'),  # browsable API root
    path('', include(router.urls)),
]
