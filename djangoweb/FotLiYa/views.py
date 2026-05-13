from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone

from .forms import SignUpForm
from .models import GameSession, Player, Question, Answer, ProposedQuestion

def home(request):
    return render(request, "FotLiYa/home.html")

def user_login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect("home")

        return render(request, "FotLiYa/login.html", {
            "error": "Usuari o contrasenya incorrectes"
        })

    return render(request, "FotLiYa/login.html")

def user_logout(request):
    logout(request)
    return redirect("home")

def register(request):
    form = SignUpForm()

    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("home")

    return render(request, "FotLiYa/register.html", {"form": form})

def game_setup(request):
    if request.method == "POST":
        try:
            num_players = int(request.POST.get("num_players"))
        except (TypeError, ValueError):
            num_players = 0

        if num_players < 2:
            return render(request, "FotLiYa/game_setup.html", {
                "error": "Mínim 2 jugadors"
            })

        if num_players > 20:
            num_players = 20

        request.session["num_players"] = num_players
        return redirect("game_names")

    return render(request, "FotLiYa/game_setup.html")

def game_names(request):
    num_players = request.session.get("num_players")

    if not num_players:
        return redirect("game_setup")

    return render(request, "FotLiYa/game_names.html", {
        "range_players": range(num_players)
    })

def save_players_names(request):
    if request.method == "POST":
        num_players = request.session.get("num_players")

        if not num_players:
            return redirect("game_setup")

        players = []

        for i in range(num_players):
            name = (request.POST.get(f"player_{i}") or "").strip()

            if not name:
                return render(request, "FotLiYa/game_names.html", {
                    "range_players": range(num_players),
                    "error": "Omple tots els noms"
                })

            players.append(name)

        request.session["players"] = players

        session = GameSession.objects.create(
            user=request.user if request.user.is_authenticated else None,
            started_at=timezone.now()
        )

        for name in players:
            Player.objects.create(session=session, name=name)

        request.session["game_session_id"] = session.id

        return redirect("game")

    return redirect("game_names")

def game(request):
    players = request.session.get("players", [])

    if not players:
        return redirect("game_setup")

    question = "🔥 Quin és el teu gènere musical per escalfar la prèvia?"

    return render(request, "FotLiYa/game.html", {
        "players": players,
        "question": question,
    })


def finish_game(request):
    if request.method == "POST":
        session_id = request.session.get("game_session_id")

        if session_id:
            session = GameSession.objects.filter(id=session_id).first()

            if session and not session.ended:
                session.ended = True
                session.save()

        request.session.pop("players", None)
        request.session.pop("num_players", None)
        request.session.pop("game_session_id", None)

        return redirect("home")

    return redirect("game")

@staff_member_required
def admin_question_list(request):
    questions = ProposedQuestion.objects.filter(
        status="pending"
    ).order_by("-created_at")

    return render(request, "FotLiYa/admin_question_list.html", {
        "questions": questions
    })

@staff_member_required
def approve_question(request, pk):
    proposed = get_object_or_404(ProposedQuestion, pk=pk)

    if proposed.status != "pending":
        messages.warning(request, "Ja processada")
        return redirect("admin_questions")

    Question.objects.create(
        text=proposed.text,
        active=True,
    )

    proposed.status = "approved"
    proposed.admin_note = ""
    proposed.save()

    messages.success(request, "Pregunta aprovada")
    return redirect("admin_questions")

@staff_member_required
def reject_question(request, pk):
    proposed = get_object_or_404(ProposedQuestion, pk=pk)

    if proposed.status != "pending":
        messages.warning(request, "Ja processada")
        return redirect("admin_questions")

    if request.method == "POST":
        proposed.status = "rejected"
        proposed.admin_note = request.POST.get("admin_note", "")
        proposed.save()

        messages.success(request, "Pregunta rebutjada")
        return redirect("admin_questions")

    return render(request, "FotLiYa/admin_reject_form.html", {
        "proposed": proposed
    })

def logout_confirm(request):
    return render(request, "FotLiYa/logout_confirm.html")