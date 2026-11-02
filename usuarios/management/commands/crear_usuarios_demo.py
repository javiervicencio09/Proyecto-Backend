from django.core.management.base import BaseCommand
from django.contrib.auth.models import User, Group

class Command(BaseCommand):
    help = 'Crea usuarios de demostración para los 3 perfiles (admin_demo, supervisor_demo, operativo_demo).'

    def handle(self, *args, **kwargs):
        usuarios_datos = [
            ('admin_demo', 'admin123', 'Administrador', 'admin@inmobiliariacoquimbo.cl', True),
            ('supervisor_demo', 'super123', 'Supervisor', 'supervisor@inmobiliariacoquimbo.cl', False),
            ('operativo_demo', 'oper123', 'Administrativo', 'operativo@inmobiliariacoquimbo.cl', False),
        ]

        for username, password, rol_name, email, is_super in usuarios_datos:
            user, created = User.objects.get_or_create(username=username, defaults={'email': email})
            user.set_password(password)
            user.email = email
            if is_super:
                user.is_superuser = True
                user.is_staff = True
            user.save()

            grupo, _ = Group.objects.get_or_create(name=rol_name)
            user.groups.set([grupo])

            estado = 'creado' if created else 'actualizado'
            self.stdout.write(self.style.SUCCESS(
                f'Usuario "{username}" {estado} | Contraseña: "{password}" | Rol: {rol_name}'
            ))

