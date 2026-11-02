from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User, Group
from zonas.models import Zona

class ZonasCRUDTestCase(TestCase):
    def setUp(self):
        self.client = Client()

        self.grupo_admin = Group.objects.create(name='Administrador')
        self.grupo_supervisor = Group.objects.create(name='Supervisor')
        self.grupo_administrativo = Group.objects.create(name='Administrativo')

        self.user_admin = User.objects.create_user(username='admin_test', password='password123')
        self.user_admin.groups.add(self.grupo_admin)

        self.user_supervisor = User.objects.create_user(username='super_test', password='password123')
        self.user_supervisor.groups.add(self.grupo_supervisor)

        self.user_administrativo = User.objects.create_user(username='adminis_test', password='password123')
        self.user_administrativo.groups.add(self.grupo_administrativo)

        self.zona = Zona.objects.create(
            nombre='La Serena Centro',
            destacado='Cercano a plaza de armas y museos',
            nivel_demanda='Alta'
        )

    def test_lista_muestra_zonas(self):
        response = self.client.get(reverse('zonas:lista'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'La Serena Centro')

    def test_busqueda_zonas(self):
        response = self.client.get(reverse('zonas:lista'), {'q': 'Centro'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'La Serena Centro')

        response_vacio = self.client.get(reverse('zonas:lista'), {'q': 'NoExiste'})
        self.assertContains(response_vacio, 'No se encontraron zonas')

    def test_crear_zona_por_supervisor(self):
        self.client.login(username='super_test', password='password123')
        data = {
            'nombre': 'Coquimbo Puerto',
            'destacado': 'Sector costero con amplia oferta gastronómica',
            'nivel_demanda': 'Media'
        }
        response = self.client.post(reverse('zonas:crear'), data, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(Zona.objects.filter(nombre='Coquimbo Puerto').exists())

    def test_editar_zona_por_supervisor(self):
        self.client.login(username='super_test', password='password123')
        data = {
            'nombre': 'La Serena Casco Histórico',
            'destacado': 'Patrimonio arquitectónico renovado',
            'nivel_demanda': 'Alta'
        }
        response = self.client.post(reverse('zonas:editar', args=[self.zona.id]), data, follow=True)
        self.assertEqual(response.status_code, 200)
        self.zona.refresh_from_db()
        self.assertEqual(self.zona.nombre, 'La Serena Casco Histórico')

    def test_eliminar_zona_restringido_para_supervisor(self):
        # La eliminación de zonas es una operación crítica reservada para el Administrador
        self.client.login(username='super_test', password='password123')
        response = self.client.post(reverse('zonas:eliminar', args=[self.zona.id]), follow=True)
        self.assertTrue(Zona.objects.filter(id=self.zona.id).exists())
        self.assertContains(response, 'Acceso denegado')

    def test_eliminar_zona_por_admin(self):
        self.client.login(username='admin_test', password='password123')
        response = self.client.post(reverse('zonas:eliminar', args=[self.zona.id]), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(Zona.objects.filter(id=self.zona.id).exists())
