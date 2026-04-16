from django.contrib import admin
from .models import GameSession, Player, Question, Answer


class PlayerInline(admin.TabularInline):
    model = Player
    extra = 0


@admin.register(GameSession)
class GameSessionAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "created_at", "duration_seconds", "ended")
    list_filter = ("ended", "created_at")


@admin.register(Player)
class PlayerAdmin(admin.ModelAdmin):
    list_display = ("name", "session", "score")


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ("text", "active")


@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ("player", "question", "session", "created_at")