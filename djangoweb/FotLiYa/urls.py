from django.urls import path
from FotLiYa import views

urlpatterns = [
    path("", views.home, name="home"),
    path("login/", views.user_login, name="login"),
    path("logout/", views.user_logout, name="logout"),
    path("logout/confirm/", views.logout_confirm, name="logout_confirm"),
    path("register/", views.register, name="register"),
    path("game/setup/", views.game_setup, name="game_setup"),
    path("game/names/", views.game_names, name="game_names"),
    path("game/names/save/", views.save_players_names, name="save_players_names"),
    path("game/finish/", views.finish_game, name="finish_game"),
    path("game/", views.game, name="game"),
    path("game/add_player/", views.add_player, name="add_player"),
]