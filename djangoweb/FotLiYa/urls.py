from django.contrib import admin
from django.urls import path
from FotLiYa import views

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', views.home, name='home'),

    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('logout/confirm/', views.logout_confirm, name='logout_confirm'),

    path('register/', views.register, name='register'),  # 🔥 AQUEST ÉS EL QUE FALTAVA

    path('game/setup/', views.game_setup, name='game_setup'),
    path('game/', views.game, name='game'),
]