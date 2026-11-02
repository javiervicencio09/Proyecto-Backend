from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User, Group

class AutenticacionYRolesTestCase(TestCase):
    def setUp(self):
        self.client = Client()

        self.grupo_admin = Group.objects.create(name='Administrador')
        self.grupo_supervisor = Group.objects.create(name='Supervisor')
        self.grupo_administrativo = Group.objects.create(name='Administrativo')

        self.user_admin = User.objects.create_user(username='admin_test', password='password123')
        self.user_admin.groups.add(self.grupo_admin)

        self.user_supervisor = User.objects.create_user(username='supervisor_test', password='password123')
        self.user_supervisor.groups.add(self.grupo_supervisor)

        self.user_administrativo = User.objects.create_user(username='adminis_test', password='password123')
        self.user_administrativo.groups.add(self.grupo_administrativo)

    def test_pantalla_login_carga_correctamente(self):
        response = self.client.get(reverse('usuarios:login'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Acceso al Sistema')

    def test_redireccion_dashboard_admin(self):
        self.client.login(username='admin_test', password='password123')
        response = self.client.get(reverse('usuarios:dashboard'), follow=True)
        self.assertRedirects(response, reverse('usuarios:dashboard_admin'))
        self.assertContains(response, 'Panel de Control Global')

    def test_redireccion_dashboard_supervisor(self):
        self.client.login(username='supervisor_test', password='password123')
        response = self.client.get(reverse('usuarios:dashboard'), follow=True)
        self.assertRedirects(response, reverse('usuarios:dashboard_supervisor'))
        self.assertContains(response, 'Panel de Control Operacional')

    def test_redireccion_dashboard_administrativo(self):
        self.client.login(username='adminis_test', password='password123')
        response = self.client.get(reverse('usuarios:dashboard'), follow=True)
        self.assertRedirects(response, reverse('usuarios:dashboard_administrativo'))
        self.assertContains(response, 'Panel de Operaciones Diarias')

    def test_restriccion_administrativo_no_puede_entrar_a_admin(self):
        self.client.login(username='adminis_test', password='password123')
        # Intenta entrar al panel de administrador
        response = self.client.get(reverse('usuarios:dashboard_admin'), follow=True)
        # Debe redirigir y mostrar mensaje de error
        self.assertRedirects(response, reverse('usuarios:dashboard_administrativo'))
        self.assertContains(response, 'Acceso denegado')
