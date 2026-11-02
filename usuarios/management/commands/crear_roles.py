from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from propiedades.models import Propiedad
from zonas.models import Zona

class Command(BaseCommand):
    help = 'Crea los 3 grupos requeridos (Administrador, Supervisor, Administrativo) y configura sus permisos base.'

    def handle(self, *args, **kwargs):
        roles = ['Administrador', 'Supervisor', 'Administrativo']
        creados = 0

        for rol in roles:
            grupo, created = Group.objects.get_or_create(name=rol)
            if created:
                creados += 1
                self.stdout.write(self.style.SUCCESS(f'Grupo "{rol}" creado con éxito.'))
            else:
                self.stdout.write(self.style.WARNING(f'Grupo "{rol}" ya existía.'))

        # Asignar permisos básicos a Supervisor y Administrativo
        propiedad_ct = ContentType.objects.get_for_model(Propiedad)
        zona_ct = ContentType.objects.get_for_model(Zona)

        # Supervisor: view, add, change en Propiedad y Zona
        supervisor_group = Group.objects.get(name='Supervisor')
        supervisor_perms = Permission.objects.filter(
            content_type__in=[propiedad_ct, zona_ct],
            codename__in=['view_propiedad', 'add_propiedad', 'change_propiedad',
                          'view_zona', 'add_zona', 'change_zona']
        )
        supervisor_group.permissions.set(supervisor_perms)

        # Administrativo: view en ambas, add en Propiedad (sin delete ni admin)
        admin_group = Group.objects.get(name='Administrativo')
        admin_perms = Permission.objects.filter(
            content_type__in=[propiedad_ct, zona_ct],
            codename__in=['view_propiedad', 'view_zona', 'add_propiedad']
        )
        admin_group.permissions.set(admin_perms)

        # Administrador: todos los permisos
        administrador_group = Group.objects.get(name='Administrador')
        todos_perms = Permission.objects.filter(content_type__in=[propiedad_ct, zona_ct])
        administrador_group.permissions.set(todos_perms)

        self.stdout.write(self.style.SUCCESS(f'Configuración de grupos y permisos completada ({creados} creados).'))

