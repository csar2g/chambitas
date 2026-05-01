from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from .models import Link, Perfil
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

    return {
        "perfil": perfil,
        "portfolio_url": portfolio_link.url if portfolio_link else "",
        "linkedin_url": linkedin_link.url if linkedin_link else "",
        "aptitudes": aptitudes,
        "aptitudes_texto": ", ".join(aptitudes),
        "usuario_mensajes_id": usuario_mensajes.id,
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
