from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User, Group
from django.core import mail
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes

class AutenticacionYRolesTestCase(TestCase):
    def setUp(self):
        self.client = Client()

        self.grupo_admin = Group.objects.create(name='Administrador')
        self.grupo_supervisor = Group.objects.create(name='Supervisor')
        self.grupo_administrativo = Group.objects.create(name='Administrativo')

        self.user_admin = User.objects.create_user(
            username='admin_test',
            email='admin@correo.cl',
            password='password123'
        )
        self.user_admin.groups.add(self.grupo_admin)

        self.user_supervisor = User.objects.create_user(
            username='supervisor_test',
            email='supervisor@correo.cl',
            password='password123'
        )
        self.user_supervisor.groups.add(self.grupo_supervisor)

        self.user_administrativo = User.objects.create_user(
            username='adminis_test',
            email='adminis@correo.cl',
            password='password123'
        )
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
        response = self.client.get(reverse('usuarios:dashboard_admin'), follow=True)
        self.assertRedirects(response, reverse('usuarios:dashboard_administrativo'))
        self.assertContains(response, 'Acceso denegado')

    # --- Pruebas de Gestión de Usuarios (Exclusivo Administrador) ---
    def test_admin_puede_crear_usuario_con_rol(self):
        self.client.login(username='admin_test', password='password123')
        data = {
            'username': 'nuevo_super',
            'email': 'nuevo@correo.cl',
            'first_name': 'Nuevo',
            'last_name': 'Supervisor',
            'rol': 'Supervisor',
            'password': 'passwordSegura123',
            'password_confirm': 'passwordSegura123',
        }
        response = self.client.post(reverse('usuarios:crear_usuario'), data, follow=True)
        self.assertEqual(response.status_code, 200)

        nuevo = User.objects.filter(username='nuevo_super').first()
        self.assertIsNotNone(nuevo)
        self.assertTrue(nuevo.groups.filter(name='Supervisor').exists())

    def test_supervisor_no_puede_acceder_a_gestion_usuarios(self):
        self.client.login(username='supervisor_test', password='password123')
        response = self.client.get(reverse('usuarios:lista_usuarios'), follow=True)
        self.assertRedirects(response, reverse('usuarios:dashboard_supervisor'))
        self.assertContains(response, 'Acceso denegado')

    # --- Pruebas de Recuperación de Contraseña (Email + Token) ---
    def test_solicitud_recuperacion_contrasena_envia_correo(self):
        response = self.client.post(
            reverse('usuarios:password_reset'),
            {'email': 'supervisor@correo.cl'},
            follow=True
        )
        self.assertEqual(response.status_code, 200)
        self.assertRedirects(response, reverse('usuarios:password_reset_done'))
        self.assertContains(response, '¡Enlace Enviado!')
        self.assertEqual(len(mail.outbox), 1)
        self.assertIn('Recuperación de contraseña', mail.outbox[0].subject)

    def test_confirmacion_cambio_clave_con_token(self):
        uid = urlsafe_base64_encode(force_bytes(self.user_supervisor.pk))
        token = default_token_generator.make_token(self.user_supervisor)

        url_confirm = reverse('usuarios:password_reset_confirm', kwargs={'uidb64': uid, 'token': token})
        response = self.client.get(url_confirm, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Establecer Nueva Contraseña')

        # Establecer la nueva contraseña en la URL redirigida sin token visible
        url_formulario = response.redirect_chain[0][0]
        response_post = self.client.post(url_formulario, {
            'new_password1': 'nuevaClaveSuper456',
            'new_password2': 'nuevaClaveSuper456',
        }, follow=True)
        self.assertEqual(response_post.status_code, 200)
        self.assertRedirects(response_post, reverse('usuarios:password_reset_complete'))

        # Probar que puede loguearse con la nueva contraseña
        login_exitoso = self.client.login(username='supervisor_test', password='nuevaClaveSuper456')
        self.assertTrue(login_exitoso)
