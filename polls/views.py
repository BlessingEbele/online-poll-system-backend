# polls/views.py
from rest_framework import viewsets, permissions, serializers
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import SAFE_METHODS, BasePermission

from drf_spectacular.utils import (
    extend_schema_view,
    extend_schema,
    OpenApiResponse,
    OpenApiExample,
)

from .models import Poll, Option, Vote
from .serializers import PollSerializer, OptionSerializer, VoteSerializer, APIRootSerializer

# -----------------------
# API Root
# -----------------------

@extend_schema(
    responses=APIRootSerializer,
    examples=[
        OpenApiExample(
            "API Root Example",
            value={
                "polls": "http://localhost:8000/api/polls/",
                "options": "http://localhost:8000/api/options/",
                "votes": "http://localhost:8000/api/votes/",
            },
        )
    ],
)
@api_view(["GET"])
def api_root(request, format=None):
    return Response({
        "polls": request.build_absolute_uri("/api/polls/"),
        "options": request.build_absolute_uri("/api/options/"),
        "votes": request.build_absolute_uri("/api/votes/"),
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
class IsReadOnlyOrVoteAllowed(BasePermission):
    """
    Custom permission:
    - Allow safe methods (GET, HEAD, OPTIONS) for anyone
    - Allow POST (vote creation) for anyone (session-based auth)
    - Require authentication for destructive methods (PUT, PATCH, DELETE)
    """
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        if request.method == "POST":
            return True
        return request.user and request.user.is_authenticated


@extend_schema_view(
    list=extend_schema(
        summary="List votes",
        tags=["Votes"],
        description="Retrieve all votes. No authentication required."
    ),
    create=extend_schema(
        summary="Cast a vote",
        tags=["Votes"],
        description=(
            "Cast a vote for a poll option.\n\n"
            "- **No login required** — votes are tracked by session key.\n"
            "- If no session exists, one is created automatically.\n"
            "- Duplicate votes within the same session are blocked."
        ),
        examples=[
            OpenApiExample(
                "Vote Example",
                value={"option": 1},
                request_only=True,
                response_only=False,
            ),
        ],
        responses={
            201: OpenApiResponse(description="Vote successfully created"),
            400: OpenApiResponse(description="Invalid input or duplicate vote in this session"),
        },
    ),
    destroy=extend_schema(
        summary="Delete a vote",
        tags=["Votes"],
        description=(
            "Delete a vote. **Authentication required.**\n\n"
            "- Authenticated users may delete votes they own (if ownership rules apply).\n"
            "- Anonymous users will receive **403 Forbidden**."
        ),
        responses={
            204: OpenApiResponse(description="Vote deleted"),
            403: OpenApiResponse(description="Forbidden: authentication required"),
        },
    ),
    partial_update=extend_schema(
        summary="Update a vote",
        tags=["Votes"],
        description=(
            "Partially update a vote. **Authentication required.**\n\n"
            "Anonymous users will receive **403 Forbidden**."
        ),
        responses={
            200: OpenApiResponse(description="Vote updated"),
            403: OpenApiResponse(description="Forbidden: authentication required"),
        },
    ),
)
class VoteViewSet(viewsets.ModelViewSet):
    queryset = Vote.objects.all()
    serializer_class = VoteSerializer
    permission_classes = [IsReadOnlyOrVoteAllowed]

    def perform_create(self, serializer):
        option = serializer.validated_data.get('option')
        request = self.request

        if not option:
            raise ValidationError("Option must be provided.")

        # Ensure session exists
        if not request.session.session_key:
            request.session.create()

        serializer.save(session_key=request.session.session_key)
