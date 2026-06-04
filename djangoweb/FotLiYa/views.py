from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from .api_client import get_random_game
from .forms import SignUpForm, RejectQuestionForm, ProposedQuestionForm
from .models import GameSession, Player, Question, ProposedQuestion


def home(request):
    total_questions = Question.objects.filter(active=True).count()
    total_sessions = GameSession.objects.filter(ended=True).count()
    total_players = Player.objects.count()
    return render(request, "FotLiYa/home.html", {
        "total_questions": total_questions,
        "total_sessions": total_sessions,
        "total_players": total_players,
    })


def user_login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect("home")

        return render(
            request,
            "FotLiYa/login.html",
            {"error": "Usuari o contrasenya incorrectes"},
        )

    return render(request, "FotLiYa/login.html")


def user_logout(request):
    logout(request)
    return redirect("home")


def logout_confirm(request):
    return render(request, "FotLiYa/logout_confirm.html")


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
            return render(
                request,
                "FotLiYa/game_setup.html",
                {"error": "Mínim 2 jugadors"},
            )

        if num_players > 20:
            num_players = 20

        request.session["num_players"] = num_players
        return redirect("game_names")

    return render(request, "FotLiYa/game_setup.html")


def game_names(request):
    num_players = request.session.get("num_players")

    if not num_players:
        return redirect("game_setup")

    return render(
        request,
        "FotLiYa/game_names.html",
        {"range_players": range(num_players)},
    )


def save_players_names(request):
    if request.method == "POST":
        num_players = request.session.get("num_players")

        if not num_players:
            return redirect("game_setup")

        players = []

        for i in range(num_players):
            name = (request.POST.get(f"player_{i}") or "").strip()

            if not name:
                return render(
                    request,
                    "FotLiYa/game_names.html",
                    {
                        "range_players": range(num_players),
                        "error": "Omple tots els noms",
                    },
                )

            players.append(name)

        request.session["players"] = players

        session = GameSession.objects.create(
            user=request.user if request.user.is_authenticated else None,
        )

        for name in players:
            Player.objects.create(session=session, name=name)

        request.session["game_session_id"] = session.id
        request.session["current_turn_index"] = 0
        request.session["round_number"] = 1

        return redirect("game")

    return redirect("game_names")


def game(request):
    players = request.session.get("players", [])

    if not players:
        return redirect("game_setup")

    current_turn_index = request.session.get("current_turn_index", 0)
    round_number = request.session.get("round_number", 1)

    if current_turn_index >= len(players):
        current_turn_index = 0

    current_player = players[current_turn_index]

    game = get_random_game(players)

    if not game:
        game = {
            "title": "Pregunta",
            "body": "🔥 Quin és el teu gènere musical per escalfar la prèvia?"
        }

    if not game.get("body"):
        game["body"] = "🔥 No hi ha pregunta disponible ara mateix."

    if "title" not in game or not game["title"]:
        game["title"] = "Pregunta"

    next_turn_index = current_turn_index + 1
    next_round_number = round_number

    if next_turn_index >= len(players):
        next_turn_index = 0
        next_round_number += 1

    request.session["current_turn_index"] = next_turn_index
    request.session["round_number"] = next_round_number

    return render(
        request,
        "FotLiYa/game.html",
        {
            "players": players,
            "game": game,
            "current_player": current_player,
            "round_number": round_number,
        },
    )

def add_player(request):
    if request.method == "POST":
        name = (request.POST.get("new_player") or "").strip()
        session_id = request.session.get("game_session_id")

        if name and session_id:
            game_session = GameSession.objects.filter(id=session_id).first()

            if game_session:
                Player.objects.create(
                    session=game_session,
                    name=name,
                )

                players = request.session.get("players", [])
                players.append(name)
                request.session["players"] = players

    return redirect("game")


def finish_game(request):
    if request.method == "POST":
        session_id = request.session.get("game_session_id")

        if session_id:
            session = GameSession.objects.filter(id=session_id).first()

            if session and not session.ended:
                session.duration_seconds = 0
                session.ended = True
                session.save()

        request.session.pop("players", None)
        request.session.pop("num_players", None)
        request.session.pop("game_session_id", None)
        request.session.pop("current_turn_index", None)
        request.session.pop("round_number", None)

        return redirect("home")

    return redirect("game")


# ==========================
# ADMINISTRACIÓ DE PREGUNTES
# ==========================

def admin_question_list(request):
    if not request.user.is_authenticated or not request.user.is_staff:
        return redirect('login')

    proposed_questions = (
        ProposedQuestion.objects
        .filter(status="pending")
        .select_related("created_by")
        .order_by("-created_at")
    )
    return render(
        request,
        "FotLiYa/admin_question_list.html",
        {
            "questions": proposed_questions,
        },
    )


def approve_question(request, pk):
    if not request.user.is_authenticated or not request.user.is_staff:
        return redirect('login')

    proposed_question = get_object_or_404(
        ProposedQuestion,
        pk=pk,
        status="pending",
    )

    Question.objects.create(
        text=proposed_question.text,
        active=True,
        source="proposed",
    )

    proposed_question.status = "approved"
    proposed_question.admin_note = ""
    proposed_question.save(
        update_fields=["status", "admin_note"],
    )

    messages.success(
        request,
        "Pregunta aprovada correctament.",
    )

    return redirect("admin_questions")


def reject_question(request, pk):
    if not request.user.is_authenticated or not request.user.is_staff:
        return redirect('login')

    proposed_question = get_object_or_404(
        ProposedQuestion,
        pk=pk,
        status="pending",
    )

    if request.method == "POST":
        form = RejectQuestionForm(request.POST)

        if form.is_valid():
            proposed_question.status = "rejected"
            proposed_question.admin_note = form.cleaned_data["admin_note"]
            proposed_question.save(
                update_fields=["status", "admin_note"],
            )

            messages.success(
                request,
                "Pregunta rebutjada correctament.",
            )

            return redirect("admin_questions")
    else:
        form = RejectQuestionForm()

    return render(
        request,
        "FotLiYa/admin_reject_form.html",
        {
            "form": form,
            "proposed_question": proposed_question,
        },
    )
@login_required
def question_detail(request, pk):
    question = get_object_or_404(
        ProposedQuestion,
        pk=pk,
        created_by=request.user
    )
    return render(request, 'FotLiYa/question_detail.html', {
        'question': question
    })


# ==========================
# GESTIÓ DE PREGUNTES D'USUARI
# ==========================

@login_required
def question_list(request):
    questions = (
        ProposedQuestion.objects
        .filter(created_by=request.user)
        .order_by("-created_at")
    )

    return render(
        request,
        "FotLiYa/question_list.html",
        {
            "questions": questions,
        },
    )


@login_required
def question_create(request):
    if request.method == "POST":
        form = ProposedQuestionForm(request.POST)

        if form.is_valid():
            proposed_question = form.save(commit=False)
            proposed_question.created_by = request.user
            proposed_question.save()

            messages.success(
                request,
                "Pregunta enviada correctament i pendent de revisió.",
            )

            return redirect("question_list")
    else:
        form = ProposedQuestionForm()

    return render(
        request,
        "FotLiYa/question_form.html",
        {
            "form": form,
        },
    )


@login_required
def question_edit(request, pk):
    question = get_object_or_404(
        ProposedQuestion,
        pk=pk,
        created_by=request.user,
    )

    if question.status != "pending":
        messages.error(
            request,
            "Només pots editar preguntes pendents.",
        )
        return redirect("question_list")

    if request.method == "POST":
        form = ProposedQuestionForm(
            request.POST,
            instance=question,
        )

        if form.is_valid():
            form.save()

            messages.success(
                request,
                "Pregunta actualitzada correctament.",
            )

            return redirect("question_list")
    else:
        form = ProposedQuestionForm(instance=question)

    return render(
        request,
        "FotLiYa/question_form.html",
        {
            "form": form,
        },
    )


@login_required
def question_delete(request, pk):
    question = get_object_or_404(
        ProposedQuestion,
        pk=pk,
        created_by=request.user,
    )

    if question.status != "pending":
        messages.error(
            request,
            "Només pots eliminar preguntes que estiguin pendents.",
        )
        return redirect("question_list")

    if request.method == "POST":
        question.delete()

        messages.success(
            request,
            "Pregunta eliminada correctament.",
        )

        return redirect("question_list")

    return render(
        request,
        "FotLiYa/question_confirm_delete.html",
        {
            "question": question,
        },
    )

@login_required
def stats(request):
    sessions = (
        GameSession.objects
        .filter(user=request.user)
        .prefetch_related("players")
        .order_by("-created_at")
    )

    total_sessions = sessions.count()
    total_players = sum(session.players.count() for session in sessions)

    return render(
        request,
        "FotLiYa/stats.html",
        {
            "sessions": sessions,
            "total_sessions": total_sessions,
            "total_players": total_players,
        },
    )