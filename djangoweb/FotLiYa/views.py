from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from django.shortcuts import render, redirect

def game_setup(request):
    if request.method == "POST":
        num_players = int(request.POST.get("num_players"))

        players = []
        for i in range(num_players):
            name = request.POST.get(f"player_{i}")
            players.append(name)

        request.session["players"] = players

        return redirect("game")

    return render(request, "FotLiYa/game_setup.html")


def game(request):
    players = request.session.get("players", [])

    question = "Quin és el teu gènere musical preferit per ballar?"

    return render(request, "FotLiYa/game.html", {
        "question": question,
        "players": players
    })
# -------------------------
# REGISTER
# -------------------------
def register(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        if User.objects.filter(username=username).exists():
            return render(request, "FotLiYa/register.html", {
                "error": "Aquest usuari ja existeix"
            })

        user = User.objects.create_user(username=username, password=password)
        user.save()

        return redirect("game")

    return render(request, "FotLiYa/register.html")


# -------------------------
# HOME
# -------------------------
def home(request):
    return render(request, "FotLiYa/home.html")


# -------------------------
# LOGIN
# -------------------------
def user_login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        # usuari hardcoded de prova
        if username == "user1" and password == "user1":

            user, created = User.objects.get_or_create(username="user1")

            if created:
                user.set_password("user1")
                user.save()

            user = authenticate(request, username="user1", password="user1")

            if user is not None:
                login(request, user)
                return redirect("game")

        return render(request, "FotLiYa/login.html", {
            "error": "Usuari o contrasenya incorrectes"
        })

    return render(request, "FotLiYa/login.html")


# -------------------------
# LOGOUT
# -------------------------
def user_logout(request):
    logout(request)
    return redirect("home")


def logout_confirm(request):
    return render(request, "FotLiYa/logout_confirm.html")


# -------------------------
# GAME (PROTECTED)
# -------------------------
@login_required
def game(request):
    question = "Quin és el teu gènere musical preferit per ballar?"
    return render(request, "FotLiYa/game.html", {"question": question})