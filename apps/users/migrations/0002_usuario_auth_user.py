from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


def vincular_usuario_auth_user(apps, schema_editor):
    Usuario = apps.get_model("users", "Usuario")
    AuthUser = apps.get_model("auth", "User")

    for usuario in Usuario.objects.filter(auth_user__isnull=True):
        if not usuario.correo:
            continue
        auth_user = AuthUser.objects.filter(email__iexact=usuario.correo).first()
        if auth_user:
            usuario.auth_user = auth_user
            usuario.save(update_fields=["auth_user"])


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0001_initial"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name="usuario",
            name="auth_user",
            field=models.OneToOneField(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="usuario_app",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.RunPython(vincular_usuario_auth_user, migrations.RunPython.noop),
    ]
