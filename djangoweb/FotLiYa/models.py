from django.db import models
from django.contrib.auth.models import User


class GameSession(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    duration_seconds = models.IntegerField(null=True, blank=True)
    ended = models.BooleanField(default=False)
    game_type = models.CharField(max_length=100, blank=True, default="")

    def __str__(self):
        username = self.user.username if self.user else "anonymous"
        return f"Session {self.id} - {username}"


class Player(models.Model):
    session = models.ForeignKey(GameSession, on_delete=models.CASCADE, related_name="players")
    name = models.CharField(max_length=50)
    score = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.name} (session {self.session.id})"


class Question(models.Model):
    SOURCE_CHOICES = [
        ("api", "API"),
        ("proposed", "Proposed"),
    ]

    text = models.CharField(max_length=255)
    active = models.BooleanField(default=True)
    source = models.CharField(max_length=20, choices=SOURCE_CHOICES, default="api")

    def __str__(self):
        return self.text


class Answer(models.Model):
    session = models.ForeignKey(GameSession, on_delete=models.CASCADE)
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    answer_text = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.player.name} - {self.question.text}"


class ProposedQuestion(models.Model):
    STATUS_CHOICES = [
        ("pending", "Pendent"),
        ("approved", "Aprovada"),
        ("rejected", "Rebutjada"),
    ]

    text = models.TextField()
    category = models.CharField(max_length=100)
    mechanics = models.CharField(max_length=100, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="proposed_questions")
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="pending")
    admin_note = models.TextField(blank=True)

    def __str__(self):
        return f"{self.text[:50]} ({self.get_status_display()})"