# polls/views.py
from rest_framework import viewsets, permissions, serializers
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.exceptions import ValidationError
from drf_spectacular.utils import extend_schema_view, extend_schema

from .models import Poll, Option, Vote
from .serializers import PollSerializer, OptionSerializer, VoteSerializer


# -----------------------
# API Root
# -----------------------
class APIRootSerializer(serializers.Serializer):
    polls = serializers.CharField()
    options = serializers.CharField()
    votes = serializers.CharField()


@api_view(['GET'])
@extend_schema(
    summary="API Root",
    description="Links to the main resources of the API.",
    responses={200: APIRootSerializer},
)
def api_root(request, format=None):
    return Response({
        'polls': reverse('poll-list', request=request, format=format),
        'options': reverse('option-list', request=request, format=format),
        'votes': reverse('vote-list', request=request, format=format),
    })


# -----------------------
# Polls
# -----------------------
@extend_schema_view(
    list=extend_schema(summary="List all polls", tags=["Polls"]),
    create=extend_schema(summary="Create a new poll (auth required)", tags=["Polls"]),
)
class PollViewSet(viewsets.ModelViewSet):
    queryset = Poll.objects.all().order_by('-pub_date')
    serializer_class = PollSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


# -----------------------
# Options
# -----------------------
@extend_schema_view(
    list=extend_schema(summary="List all options", tags=["Options"]),
    create=extend_schema(summary="Create a new option (auth required)", tags=["Options"]),
)
class OptionViewSet(viewsets.ModelViewSet):
    queryset = Option.objects.all()
    serializer_class = OptionSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


# -----------------------
# Votes
# -----------------------
@extend_schema_view(
    list=extend_schema(summary="List votes", tags=["Votes"]),
    create=extend_schema(summary="Cast a vote (auth required)", tags=["Votes"]),
)
class VoteViewSet(viewsets.ModelViewSet):
    queryset = Vote.objects.all()
    serializer_class = VoteSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        option = serializer.validated_data.get('option')
        request = self.request

        if not option:
            raise ValidationError("Option must be provided.")

        # Ensure session exists
        if not request.session.session_key:
            request.session.create()

        serializer.save(session_key=request.session.session_key)
