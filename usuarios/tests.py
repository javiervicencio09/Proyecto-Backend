from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User, Group
from django.core import mail

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

    # --- Pruebas de Recuperación de Contraseña con Código de 5 Dígitos ---
    def test_solicitud_recuperacion_envia_codigo_de_5_digitos(self):
        response = self.client.post(
            reverse('usuarios:password_reset'),
            {'email': 'supervisor@correo.cl'},
            follow=True
        )
        self.assertEqual(response.status_code, 200)
        self.assertRedirects(response, reverse('usuarios:password_reset_codigo'))
        self.assertContains(response, 'Ingresa tu Código de Seguridad')

        # Verificar que se envió un correo
        self.assertEqual(len(mail.outbox), 1)
        # Verificar que el código tiene 5 dígitos
        session = self.client.session
        codigo = session.get('reset_code')
        self.assertIsNotNone(codigo)
        self.assertEqual(len(codigo), 5)
        self.assertIn(codigo, mail.outbox[0].body)

    def test_verificar_codigo_correcto_cambia_password(self):
        # 1. Solicitar código
        self.client.post(reverse('usuarios:password_reset'), {'email': 'supervisor@correo.cl'})
        codigo = self.client.session.get('reset_code')

        # 2. Enviar código y nueva clave
        response = self.client.post(reverse('usuarios:password_reset_codigo'), {
            'codigo': codigo,
            'new_password1': 'nuevaClaveSuper456',
            'new_password2': 'nuevaClaveSuper456',
        }, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertRedirects(response, reverse('usuarios:login'))
        self.assertContains(response, '¡Tu contraseña ha sido restablecida con éxito!')

        # 3. Probar inicio de sesión con nueva contraseña
        login_exitoso = self.client.login(username='supervisor_test', password='nuevaClaveSuper456')
        self.assertTrue(login_exitoso)

    def test_verificar_codigo_incorrecto_muestra_error(self):
        # 1. Solicitar código
        self.client.post(reverse('usuarios:password_reset'), {'email': 'supervisor@correo.cl'})

        # 2. Enviar código erróneo
        response = self.client.post(reverse('usuarios:password_reset_codigo'), {
            'codigo': '99999',
            'new_password1': 'nuevaClaveSuper456',
            'new_password2': 'nuevaClaveSuper456',
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'El código de 5 dígitos ingresado es incorrecto.')
