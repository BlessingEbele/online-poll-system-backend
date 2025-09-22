from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Poll, Option, Vote
from django.contrib.auth.models import User


User = get_user_model()

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
    user = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Vote
        fields = ['id', 'user', 'option']

    def validate(self, data):
        option = data.get('option')
        user = self.context['request'].user
        if not option:
            raise serializers.ValidationError("Vote must have an option selected.")
        # Prevent multiple votes per poll
        if Vote.objects.filter(user=user, option__poll=option.poll).exists():
            raise serializers.ValidationError("You have already voted for this poll.")
        return data

    def create(self, validated_data):
        # Auto-assign the logged-in user
        user = self.context['request'].user
        validated_data['user'] = user
        return super().create(validated_data)


class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=6)

    class Meta:
        model = User
        fields = ("username", "email", "password")

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data["username"],
            email=validated_data.get("email"),
            password=validated_data["password"],
        )
        return user
