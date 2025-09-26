# polls/models.py
from django.db import models
from django.core.exceptions import ValidationError


class Poll(models.Model):
    question = models.CharField(max_length=255)
    pub_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.question


class Option(models.Model):
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE, related_name='options')
    text = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.text} (Poll: {self.poll.question})"


class Vote(models.Model):
    option = models.ForeignKey(Option, on_delete=models.CASCADE, related_name='votes')
    # Store session key instead of user (since we dropped auth)
    session_key = models.CharField(max_length=40, null=True, blank=True)
    voted_at = models.DateTimeField(auto_now_add=True)

    def clean(self):
        if self.option is None:
            raise ValidationError("Vote must be linked to an Option.")

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Session {self.session_key} voted for {self.option.text}"
