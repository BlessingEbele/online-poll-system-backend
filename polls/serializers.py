# polls/serializers.py
from rest_framework import serializers
from .models import Poll, Option, Vote


class OptionSerializer(serializers.ModelSerializer):
    votes_count = serializers.IntegerField(source='votes.count', read_only=True)

    class Meta:
        model = Option
        fields = ['id', 'text', 'poll', 'votes_count']


class PollSerializer(serializers.ModelSerializer):
    options = OptionSerializer(many=True, read_only=True)

    class Meta:
        model = Poll
        fields = ['id', 'question', 'pub_date', 'options']


class VoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vote
        fields = ['id', 'option']

    def validate(self, data):
        option = data.get('option')
        request = self.context.get("request")

        if not option:
            raise serializers.ValidationError("Vote must have an option selected.")

        # Ensure session exists
        if not request.session.session_key:
            request.session.create()

        session_key = request.session.session_key

        # Prevent multiple votes per poll by the same session
        if Vote.objects.filter(session_key=session_key, option__poll=option.poll).exists():
            raise serializers.ValidationError("You have already voted for this poll.")

        return data
