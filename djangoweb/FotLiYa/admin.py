from django.contrib import admin
from .models import GameSession, Player, Question, Answer, ProposedQuestion


class PlayerInline(admin.TabularInline):
    model = Player
    extra = 0


@admin.register(GameSession)
class GameSessionAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "started_at", "created_at", "duration_seconds", "ended", "game_type")
    list_filter = ("ended", "created_at", "started_at", "game_type")
    search_fields = ("user__username",)
    date_hierarchy = "started_at"
    ordering = ("-started_at",)
    inlines = [PlayerInline]


@admin.register(Player)
class PlayerAdmin(admin.ModelAdmin):
    list_display = ("name", "session", "score", "avatar", "color")
    search_fields = ("name",)
    list_filter = ("score",)
    ordering = ("session_id", "name")


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ("short_text", "active", "source")
    list_filter = ("active", "source")
    search_fields = ("text",)
    list_editable = ("active",)
    ordering = ("-id",)

    def short_text(self, obj):
        return f"{obj.text[:80]}{'…' if len(obj.text) > 80 else ''}"

    short_text.short_description = "Text"


@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ("player", "question", "session", "created_at")
    search_fields = ("player__name", "question__text")
    ordering = ("-created_at",)


@admin.register(ProposedQuestion)
class ProposedQuestionAdmin(admin.ModelAdmin):
    list_display = ("short_text", "category", "created_by", "status", "created_at")
    list_filter = ("status", "category", "created_at")
    search_fields = ("text", "category", "created_by__username")
    readonly_fields = ("created_at",)
    ordering = ("-created_at",)

    def short_text(self, obj):
        return f"{obj.text[:80]}{'…' if len(obj.text) > 80 else ''}"

    short_text.short_description = "Text"