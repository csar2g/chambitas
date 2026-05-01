from django.urls import path

from . import views

urlpatterns = [
    path(
        "perfil/configuracion-inicial/",
        views.config_initial_profile_view,
        name="profile_setup",
    ),
    path("perfil/", views.main_profile_view, name="main_profile"),
    path("perfil/editar/", views.edit_profile_view, name="edit_profile"),
]
