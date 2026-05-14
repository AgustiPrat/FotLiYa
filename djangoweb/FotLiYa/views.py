from django.contrib.auth import login, authenticate, logout
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .api_client import get_random_game
from .models import GameSession, Player, Question, Answer, ProposedQuestion
from .forms import ProposedQuestionForm

from .forms import SignUpForm
from .models import GameSession, Player, Question, Answer

def home(request):
    return render(request, "FotLiYa/home.html")


def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)

        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("home")
    else:
        form = UserCreationForm()

    return render(request, "FotLiYa/register.html", {"form": form})


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


def logout_confirm(request):
    return render(request, "FotLiYa/logout_confirm.html")


def game_setup(request):
    if request.method == "POST":
        try:
            num_players = int(request.POST.get("num_players"))
        except (TypeError, ValueError):
            num_players = 0

        if num_players < 2:
            return render(request, "FotLiYa/game_setup.html", {
                "error": "La partida ha de tenir com a mínim 2 jugadors."
            })

        if num_players > 20:
            num_players = 20

        request.session["num_players"] = num_players
        return redirect("game_names")

    return render(request, "FotLiYa/game_setup.html")


def game_names(request):
    num_players = request.session.get("num_players")

    if not num_players or num_players < 2:
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
                    "error": "Omple tots els noms abans de continuar."
                })

            players.append(name)

        # IMPORTANT: netegem sessions antigues de joc
        request.session["players"] = players

        # CREAR SESSIÓ DE PARTIDA
        game_session = GameSession.objects.create(
            user=request.user if request.user.is_authenticated else None,
        )

        # CREAR PLAYERS A BD
        for name in players:
            Player.objects.create(
                session=game_session,
                name=name,
            )

        # guardar referència de sessió
        request.session["game_session_id"] = game_session.id

        # inici del joc
        return redirect("game")

    return redirect("game_names")


def finish_game(request):
    if request.method == "POST":
        session_id = request.session.get("game_session_id")

        if session_id:
            game_session = GameSession.objects.filter(id=session_id).first()

            if game_session and not game_session.ended:
                game_session.duration_seconds = 0  # (opcional simple)
                game_session.ended = True
                game_session.save()

        request.session.pop("players", None)
        request.session.pop("num_players", None)
        request.session.pop("game_session_id", None)
        request.session.pop("game_started_at", None)

        return redirect("home")

    return redirect("game")

def game(request):
    players = request.session.get("players", [])

    if not players:
        return redirect("game_setup")

    game = get_random_game(players)

    return render(request, "FotLiYa/game.html", {
        "players": players,
        "game": game,
    })
def add_player(request):
    if request.method == "POST":
        name = (request.POST.get("new_player") or "").strip()
        session_id = request.session.get("game_session_id")

        if name and session_id:
            game_session = GameSession.objects.filter(id=session_id).first()
            if game_session:
                Player.objects.create(session=game_session, name=name)
                players = request.session.get("players", [])
                players.append(name)
                request.session["players"] = players

    return redirect("game")

@login_required
def question_list(request):
    questions = ProposedQuestion.objects.filter(
        created_by=request.user
    ).order_by('-created_at')

    return render(request, 'FotLiYa/question_list.html', {
        'questions': questions
    })

@login_required
def question_create(request):
    if request.method == 'POST':
        form = ProposedQuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.created_by = request.user
            question.save()
            messages.success(request, "Pregunta proposada correctament! L'administrador la revisarà aviat.")
            return redirect('question_list')
    else:
        form = ProposedQuestionForm()

    return render(request, 'FotLiYa/question_form.html', {
        'form': form
    })

@login_required
def question_edit(request, pk):
    question = get_object_or_404(ProposedQuestion, pk=pk, created_by=request.user)

    if question.status != 'pending':
        messages.error(request, "Només pots editar preguntes que estiguin pendents.")
        return redirect('question_list')

    if request.method == 'POST':
        form = ProposedQuestionForm(request.POST, instance=question)
        if form.is_valid():
            form.save()
            messages.success(request, "Pregunta actualitzada correctament!")
            return redirect('question_list')
    else:
        form = ProposedQuestionForm(instance=question)

    return render(request, 'FotLiYa/question_form.html', {
        'form': form
    })

@login_required
def question_delete(request, pk):
    question = get_object_or_404(ProposedQuestion, pk=pk, created_by=request.user)

    if question.status != 'pending':
        messages.error(request, "Només pots eliminar preguntes que estiguin pendents.")
        return redirect('question_list')

    if request.method == 'POST':
        question.delete()
        messages.success(request, "Pregunta eliminada correctament.")
        return redirect('question_list')

    return render(request, 'FotLiYa/question_confirm_delete.html', {
        'question': question
    })