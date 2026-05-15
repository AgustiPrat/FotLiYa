from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class GameSession(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    started_at = models.DateTimeField(default=timezone.now)
    created_at = models.DateTimeField(auto_now_add=True)
    duration_seconds = models.IntegerField(null=True, blank=True)
    ended = models.BooleanField(default=False)
    game_type = models.CharField(max_length=50, blank=True, default="classic")
    notes = models.TextField(blank=True, default="")

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        username = self.user.username if self.user else "anonymous"
        return f"Session {self.id} - {username}"


class Player(models.Model):
    session = models.ForeignKey(GameSession, on_delete=models.CASCADE, related_name="players")
    name = models.CharField(max_length=50)
    score = models.IntegerField(default=0)
    avatar = models.CharField(max_length=50, blank=True, default="")
    color = models.CharField(max_length=20, blank=True, default="")

    class Meta:
        ordering = ["id"]

    def __str__(self):
        return f"{self.name} (session {self.session.id})"


class Question(models.Model):
    SOURCE_CHOICES = [
        ("manual", "Manual"),
        ("api", "API"),
        ("proposed", "Proposada"),
    ]
    text = models.TextField()
    active = models.BooleanField(default=True)
    source = models.CharField(max_length=20, choices=SOURCE_CHOICES, default="manual", db_index=True)

    class Meta:
        ordering = ["id"]

    def __str__(self):
        return self.text


class Answer(models.Model):
    session = models.ForeignKey(GameSession, on_delete=models.CASCADE)
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    answer_text = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.player.name} - {self.question.text}"


class ProposedQuestion(models.Model):
    STATUS_CHOICES = [
        ("pending", "Pendent"),
        ("approved", "Aprovada"),
        ("rejected", "Rebutjada"),
    ]
    text = models.TextField()
    category = models.CharField(max_length=100, db_index=True)
    mechanics = models.CharField(max_length=100, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="proposed_questions")
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="pending", db_index=True)
    admin_note = models.TextField(blank=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.text[:50]} ({self.get_status_display()})"