from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from .models import Link, Perfil, Seguimiento
from users.models import Usuario


def _build_profile_context(perfil):
    portfolio_link = perfil.links.filter(tipo=Link.TIPO_PORTFOLIO).first()
    linkedin_link = perfil.links.filter(tipo=Link.TIPO_LINKEDIN).first()
    aptitudes = [item.strip() for item in perfil.aptitudes.split(",") if item.strip()]
    auth_user = perfil.usuario
    usuario_mensajes, _ = Usuario.objects.get_or_create(
        auth_user=auth_user,
        defaults={
            "nombre": auth_user.get_full_name() or auth_user.username,
            "correo": auth_user.email or f"{auth_user.username}@chambitas.local",
        },
    )

    followers_count = Seguimiento.objects.filter(seguido=auth_user).count()
    following_count = Seguimiento.objects.filter(seguidor=auth_user).count()

    return {
        "perfil": perfil,
        "portfolio_url": portfolio_link.url if portfolio_link else "",
        "linkedin_url": linkedin_link.url if linkedin_link else "",
        "aptitudes": aptitudes,
        "aptitudes_texto": ", ".join(aptitudes),
        "usuario_mensajes_id": usuario_mensajes.id,
        "followers_count": followers_count,
        "following_count": following_count,
    }


@login_required
def config_initial_profile_view(request):
    perfil, _ = Perfil.objects.get_or_create(usuario=request.user)

    if request.method == "POST":
        action = request.POST.get("action", "draft")
        uploaded_photo = request.FILES.get("foto_perfil")
        perfil.numero_tel = request.POST.get("numero_tel", "").strip()
        perfil.whatsapp = request.POST.get("whatsapp", "").strip()
        perfil.ubicacion = request.POST.get("ubicacion", "").strip()
        perfil.descripcion = request.POST.get("descripcion", "").strip()
        perfil.aptitudes = request.POST.get("aptitudes", "").strip()
        if uploaded_photo:
            perfil.foto_perfil = uploaded_photo
        perfil.save()

        portfolio_url = request.POST.get("portfolio_url", "").strip()
        linkedin_url = request.POST.get("linkedin_url", "").strip()

        if portfolio_url:
            Link.objects.update_or_create(
                perfil=perfil,
                tipo=Link.TIPO_PORTFOLIO,
                defaults={"url": portfolio_url},
            )
        else:
            Link.objects.filter(perfil=perfil, tipo=Link.TIPO_PORTFOLIO).delete()

        if linkedin_url:
            Link.objects.update_or_create(
                perfil=perfil,
                tipo=Link.TIPO_LINKEDIN,
                defaults={"url": linkedin_url},
            )
        else:
            Link.objects.filter(perfil=perfil, tipo=Link.TIPO_LINKEDIN).delete()

        if action == "complete":
            messages.success(request, "Perfil completado. Bienvenido a Chambitas.")
            return redirect("landing")

        messages.success(request, "Borrador guardado correctamente.")
        return redirect("profile_setup")

    context = _build_profile_context(perfil)
    return render(request, "config_initial_profile.html", context)


@login_required
def main_profile_view(request):
    perfil, _ = Perfil.objects.get_or_create(usuario=request.user)
    context = _build_profile_context(perfil)
    context["is_own_profile"] = True
    context["profile_user"] = request.user
    context["is_following"] = False
    return render(request, "main_profile.html", context)


@login_required
def public_profile_view(request, user_id):
    profile_user = get_object_or_404(User, id=user_id)
    if profile_user == request.user:
        return redirect("main_profile")
    perfil, _ = Perfil.objects.get_or_create(usuario=profile_user)
    context = _build_profile_context(perfil)
    context["is_own_profile"] = False
    context["profile_user"] = profile_user
    context["is_following"] = Seguimiento.objects.filter(
        seguidor=request.user, seguido=profile_user
    ).exists()
    return render(request, "main_profile.html", context)


@login_required
def edit_profile_view(request):
    perfil, _ = Perfil.objects.get_or_create(usuario=request.user)

    if request.method == "POST":
        uploaded_photo = request.FILES.get("foto_perfil")
        perfil.descripcion = request.POST.get("descripcion", "").strip()
        perfil.numero_tel = request.POST.get("numero_tel", "").strip()
        perfil.whatsapp = request.POST.get("whatsapp", "").strip()
        perfil.ubicacion = request.POST.get("ubicacion", "").strip()
        perfil.aptitudes = request.POST.get("aptitudes", "").strip()
        if uploaded_photo:
            perfil.foto_perfil = uploaded_photo
        perfil.save()

        portfolio_url = request.POST.get("portfolio_url", "").strip()
        linkedin_url = request.POST.get("linkedin_url", "").strip()

        if portfolio_url:
            Link.objects.update_or_create(
                perfil=perfil,
                tipo=Link.TIPO_PORTFOLIO,
                defaults={"url": portfolio_url},
            )
        else:
            Link.objects.filter(perfil=perfil, tipo=Link.TIPO_PORTFOLIO).delete()

        if linkedin_url:
            Link.objects.update_or_create(
                perfil=perfil,
                tipo=Link.TIPO_LINKEDIN,
                defaults={"url": linkedin_url},
            )
        else:
            Link.objects.filter(perfil=perfil, tipo=Link.TIPO_LINKEDIN).delete()

        messages.success(request, "Perfil actualizado correctamente.")
        return redirect("main_profile")

    context = _build_profile_context(perfil)
    return render(request, "edit_profile.html", context)


@require_POST
@login_required
def toggle_follow(request, user_id):
    target_user = get_object_or_404(User, id=user_id)
    if target_user == request.user:
        return JsonResponse({"error": "No puedes seguirte a ti mismo"}, status=400)

    seguimiento = Seguimiento.objects.filter(
        seguidor=request.user, seguido=target_user
    ).first()

    if seguimiento:
        seguimiento.delete()
        following = False
    else:
        Seguimiento.objects.create(seguidor=request.user, seguido=target_user)
        following = True

    return JsonResponse(
        {
            "following": following,
            "followers_count": Seguimiento.objects.filter(seguido=target_user).count(),
        }
    )


@login_required
def followers_list(request, user_id):
    profile_user = get_object_or_404(User, id=user_id)
    seguimientos = Seguimiento.objects.filter(seguido=profile_user).select_related(
        "seguidor", "seguidor__perfil"
    )
    users = []
    for s in seguimientos:
        users.append(
            {
                "user": s.seguidor,
                "is_following": Seguimiento.objects.filter(
                    seguidor=request.user, seguido=s.seguidor
                ).exists(),
            }
        )
    return render(
        request,
        "follow_list.html",
        {
            "profile_user": profile_user,
            "users": users,
            "list_type": "followers",
            "title": f"Followers of {profile_user.get_full_name() or profile_user.username}",
        },
    )


@login_required
def following_list(request, user_id):
    profile_user = get_object_or_404(User, id=user_id)
    seguimientos = Seguimiento.objects.filter(seguidor=profile_user).select_related(
        "seguido", "seguido__perfil"
    )
    users = []
    for s in seguimientos:
        users.append(
            {
                "user": s.seguido,
                "is_following": Seguimiento.objects.filter(
                    seguidor=request.user, seguido=s.seguido
                ).exists(),
            }
        )
    return render(
        request,
        "follow_list.html",
        {
            "profile_user": profile_user,
            "users": users,
            "list_type": "following",
            "title": f"Following for {profile_user.get_full_name() or profile_user.username}",
        },
    )
