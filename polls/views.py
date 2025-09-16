from rest_framework import viewsets, permissions
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse
from .models import Poll, Option, Vote
from .serializers import PollSerializer, OptionSerializer, VoteSerializer

class PollViewSet(viewsets.ModelViewSet):
    queryset = Poll.objects.all().order_by('-pub_date')
    serializer_class = PollSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class OptionViewSet(viewsets.ModelViewSet):
    queryset = Option.objects.all()
    serializer_class = OptionSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class VoteViewSet(viewsets.ModelViewSet):
    queryset = Vote.objects.all()
    serializer_class = VoteSerializer
    permission_classes = [permissions.IsAuthenticated]# must be logged in to vote

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

@api_view(['GET'])
def api_root(request, format=None):
    """
    API Root endpoint that returns main endpoints for browsable API.
    """
    return Response({
        'polls': reverse('poll-list', request=request, format=format),
        'options': reverse('option-list', request=request, format=format),
        'votes': reverse('vote-list', request=request, format=format),
    })
