from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
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
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='votes')
    voted_at = models.DateTimeField(auto_now_add=True)

    def clean(self):
        # Validate that a Vote has an Option
        if self.option is None:
            raise ValidationError("Vote must be linked to an Option.")

    def save(self, *args, **kwargs):
        self.full_clean()  # enforce validation before saving
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user.username} voted for {self.option.text}"
