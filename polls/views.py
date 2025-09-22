# polls/views.py
from rest_framework import viewsets, permissions, generics, serializers
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.exceptions import ValidationError, PermissionDenied
from drf_spectacular.utils import extend_schema_view, extend_schema, OpenApiExample

from .permissions import IsOwnerOrReadOnly
from .models import Poll, Option, Vote
from .serializers import PollSerializer, OptionSerializer, VoteSerializer

# -----------------------
# Small serializer for API root (prevents Spectacular warning about guessing serializer)
# -----------------------
class APIRootSerializer(serializers.Serializer):
    polls = serializers.CharField()
    options = serializers.CharField()
    votes = serializers.CharField()

# -----------------------
# API Root
# -----------------------
@api_view(['GET'])
@extend_schema(
    summary="API Root",
    description="Links to the main resources of the API.",
    responses={200: APIRootSerializer},
)
def api_root(request, format=None):
    """
    API Root endpoint that returns main endpoints for browsable API.
    """
    return Response({
        'polls': reverse('poll-list', request=request, format=format),
        'options': reverse('option-list', request=request, format=format),
        'votes': reverse('vote-list', request=request, format=format),
    })

# -----------------------
# Polls
# -----------------------
@extend_schema_view(
    list=extend_schema(
        summary="List all polls",
        description="Retrieve a list of all available polls.",
        tags=["Polls"],
        responses={200: PollSerializer},
        examples=[
            OpenApiExample(
                "Poll List Example",
                value=[
                    {
                        "id": 1,
                        "question": "Who should be the next class president?",
                        "pub_date": "2025-09-20T10:00:00Z",
                        "options": [
                            {"id": 1, "text": "Candidate A", "poll": 1, "votes_count": 5},
                            {"id": 2, "text": "Candidate B", "poll": 1, "votes_count": 8}
                        ]
                    }
                ],
                response_only=True
            )
        ]
    ),
    create=extend_schema(
        summary="Create a new poll",
        description="Create a new poll. The authenticated user becomes the poll owner.",
        request=PollSerializer,
        responses={201: PollSerializer},
        tags=["Polls"],
        examples=[
            OpenApiExample(
                "Poll Create Request",
                value={"question": "Who should be the next class president?"},
                request_only=True
            ),
            OpenApiExample(
                "Poll Create Response",
                value={
                    "id": 1,
                    "question": "Who should be the next class president?",
                    "pub_date": "2025-09-20T10:00:00Z",
                    "options": []
                },
                response_only=True
            )
        ],
    ),
    retrieve=extend_schema(
        summary="Get poll details",
        description="Retrieve details of a specific poll by ID.",
        tags=["Polls"],
        responses={200: PollSerializer},
    ),
    update=extend_schema(
        summary="Update a poll",
        description="Update all fields of an existing poll (owner only).",
        request=PollSerializer,
        responses={200: PollSerializer},
        tags=["Polls"],
    ),
    partial_update=extend_schema(
        summary="Partially update a poll",
        description="Update selected fields of an existing poll (owner only).",
        request=PollSerializer,
        responses={200: PollSerializer},
        tags=["Polls"],
    ),
    destroy=extend_schema(
        summary="Delete a poll",
        description="Remove a poll permanently (owner only).",
        tags=["Polls"],
        responses={204: None},
    ),
)
class PollViewSet(viewsets.ModelViewSet):
    """
    Polls: anyone can list/retrieve.
    Creating requires authentication (owner assigned automatically).
    Update/delete require the owner.
    """
    queryset = Poll.objects.all().order_by('-pub_date')
    serializer_class = PollSerializer

    def get_permissions(self):
        # returns permission instances
        if self.action in ["list", "retrieve"]:
            return [permissions.AllowAny()]
        elif self.action == "create":
            return [permissions.IsAuthenticated()]
        else:
            # update / partial_update / destroy
            return [permissions.IsAuthenticated(), IsOwnerOrReadOnly()]

    def perform_create(self, serializer):
        # set the owner to request.user on create
        serializer.save(owner=self.request.user)


# -----------------------
# Options
# -----------------------
@extend_schema_view(
    list=extend_schema(
        summary="List all options",
        description="Retrieve all options for all polls.",
        tags=["Polls", "Options"],
        responses={200: OptionSerializer},
    ),
    create=extend_schema(
        summary="Create a new option",
        description="Add a new option to a specific poll (only poll owner allowed).",
        request=OptionSerializer,
        responses={201: OptionSerializer},
        tags=["Polls", "Options"],
        examples=[
            OpenApiExample(
                "Option Create Request",
                value={"text": "Candidate A", "poll": 1},
                request_only=True
            ),
            OpenApiExample(
                "Option Create Response",
                value={"id": 1, "text": "Candidate A", "poll": 1, "votes_count": 0},
                response_only=True
            )
        ],
    ),
    retrieve=extend_schema(
        summary="Get option details",
        description="Retrieve details of a specific option by ID.",
        tags=["Polls", "Options"],
        responses={200: OptionSerializer},
    ),
    update=extend_schema(
        summary="Update an option",
        description="Update option (only poll owner may modify).",
        request=OptionSerializer,
        responses={200: OptionSerializer},
        tags=["Polls", "Options"],
    ),
    destroy=extend_schema(
        summary="Delete an option",
        description="Delete an option (only poll owner may delete).",
        tags=["Polls", "Options"],
        responses={204: None},
    ),
)
class OptionViewSet(viewsets.ModelViewSet):
    """
    Options: list/retrieve allowed for anyone.
    Creating/Updating/Deleting requires authentication and poll ownership.
    """
    queryset = Option.objects.all()
    serializer_class = OptionSerializer

    def get_permissions(self):
        if self.action in ["list", "retrieve"]:
            return [permissions.AllowAny()]
        elif self.action == "create":
            return [permissions.IsAuthenticated()]
        else:
            # update, partial_update, destroy: ensure owner
            return [permissions.IsAuthenticated(), IsOwnerOrReadOnly()]

    def perform_create(self, serializer):
        # Ensure the user is owner of the poll they are adding an option to
        poll = serializer.validated_data.get('poll')
        if poll is None:
            raise ValidationError("Poll must be provided.")
        if poll.owner != self.request.user:
            raise PermissionDenied("Only the poll owner can add options.")
        serializer.save()


# -----------------------
# Votes
# -----------------------
@extend_schema_view(
    list=extend_schema(
        summary="List votes",
        description="(Restricted) List all votes. Typically limited to staff/admins or authenticated users.",
        tags=["Polls", "Votes"],
        responses={200: VoteSerializer},
    ),
    create=extend_schema(
        summary="Cast a vote",
        description="Vote for a specific option in a poll. Each user can only vote once per poll.",
        request=VoteSerializer,
        responses={201: VoteSerializer},
        tags=["Polls", "Votes"],
        examples=[
            OpenApiExample(
                "Vote Request",
                value={"option": 1},
                request_only=True
            ),
            OpenApiExample(
                "Vote Response",
                value={"id": 1, "option": 1, "user": 2},
                response_only=True
            )
        ],
    ),
    retrieve=extend_schema(
        summary="Get vote details",
        description="Retrieve a specific vote (owner or staff).",
        tags=["Polls", "Votes"],
        responses={200: VoteSerializer},
    ),
)
class VoteViewSet(viewsets.ModelViewSet):
    """
    Votes: creating requires authentication, and duplicates (user -> poll) are prevented.
    Listing may be limited; by default authenticated users can list (tweak if you prefer staff-only).
    """
    queryset = Vote.objects.all()
    serializer_class = VoteSerializer

    def get_permissions(self):
        if self.action in ["list", "retrieve"]:
            # You can change this to IsAdminUser() if you want only admins to list votes.
            return [permissions.IsAuthenticated()]
        elif self.action == "create":
            return [permissions.IsAuthenticated()]
        else:
            # update/destroy: only owner (voter) or staff
            return [permissions.IsAuthenticated(), IsOwnerOrReadOnly()]

    def perform_create(self, serializer):
        # Prevent duplicate votes by the same user on the same poll
        option = serializer.validated_data.get('option')
        if option is None:
            raise ValidationError("Option must be provided.")
        poll = option.poll
        user = self.request.user
        if Vote.objects.filter(user=user, option__poll=poll).exists():
            raise ValidationError("You have already voted on this poll.")
        serializer.save(user=user)
