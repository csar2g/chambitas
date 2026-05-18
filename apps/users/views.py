from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.shortcuts import redirect, render
from users.models import Usuario


def _register_context(full_name="", email="", accepted_terms=False):
    return {
        "full_name": full_name,
        "email": email,
        "accepted_terms": accepted_terms,
    }


def landing_view(request):
    if request.user.is_authenticated:
        return redirect("main_profile")
    return render(request, "landing.html")


def login_view(request):
    if request.user.is_authenticated:
        return redirect("main_profile")

    if request.method == "POST":
        email = request.POST.get("email", "").strip().lower()
        password = request.POST.get("password", "")

        if not email or not password:
            messages.error(request, "Please enter both email and password.")
            return render(request, "login.html")

        user = authenticate(request, username=email, password=password)
        if user is None:
            messages.error(request, "Invalid email or password.")
            return render(request, "login.html")

        login(request, user)
        messages.success(request, "Logged in successfully.")
        return redirect("landing")

    return render(request, "login.html")


def register_view(request):
    if request.user.is_authenticated:
        return redirect("main_profile")

    if request.method == "POST":
        full_name = request.POST.get("full_name", "").strip()
        email = request.POST.get("email", "").strip().lower()
        password = request.POST.get("password", "")
        accepted_terms = request.POST.get("terms")
        context = _register_context(
            full_name=full_name,
            email=email,
            accepted_terms=bool(accepted_terms),
        )

        if not full_name or not email or not password:
            messages.error(request, "All fields are required.")
            return render(request, "register.html", context)

        if len(password) < 8:
            messages.error(request, "Password must be at least 8 characters long.")
            return render(request, "register.html", context)

        if not accepted_terms:
            messages.error(request, "You must accept the terms to register.")
            return render(request, "register.html", context)

        if User.objects.filter(username=email).exists():
            messages.error(request, "This email is already registered.")
            return render(request, "register.html", context)

        first_name, *last_name_parts = full_name.split()
        last_name = " ".join(last_name_parts)

        user = User.objects.create_user(
            username=email,
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name,
        )
        Usuario.objects.create(
            auth_user=user,
            nombre=full_name,
            correo=email,
        )

        login(request, user)
        messages.success(request, "Account created successfully.")
        return redirect("profile_setup")

    return render(request, "register.html", _register_context())


def logout_view(request):
    if request.method == "POST":
        logout(request)
        messages.success(request, "Logged out successfully.")
    return redirect("landing")
