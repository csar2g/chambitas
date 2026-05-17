from django.urls import path

from . import views

urlpatterns = [
    path(
        "perfil/configuracion-inicial/",
        views.config_initial_profile_view,
        name="profile_setup",
    ),
    path("perfil/", views.main_profile_view, name="main_profile"),
    path("perfil/<int:user_id>/", views.public_profile_view, name="public_profile"),
    path("perfil/<int:user_id>/seguir/", views.toggle_follow, name="toggle_follow"),
    path(
        "perfil/<int:user_id>/seguidores/",
        views.followers_list,
        name="followers_list",
    ),
    path(
        "perfil/<int:user_id>/siguiendo/",
        views.following_list,
        name="following_list",
    ),
    path("perfil/editar/", views.edit_profile_view, name="edit_profile"),
]
