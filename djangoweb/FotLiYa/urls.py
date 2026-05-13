from django.contrib import admin
from django.urls import path
from FotLiYa import views

urlpatterns = [
    path("admin/", admin.site.urls),

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

    path("admin-panel/questions/", views.admin_question_list, name="admin_questions"),
    path("admin-panel/questions/<int:pk>/approve/", views.approve_question, name="approve_question"),
    path("admin-panel/questions/<int:pk>/reject/", views.reject_question, name="reject_question"),
]