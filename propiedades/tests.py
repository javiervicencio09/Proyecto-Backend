from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User, Group
from propiedades.models import Propiedad
from zonas.models import Zona

class PropiedadesCRUDTestCase(TestCase):
    def setUp(self):
        self.client = Client()

        # Roles
        self.grupo_admin = Group.objects.create(name='Administrador')
        self.grupo_supervisor = Group.objects.create(name='Supervisor')
        self.grupo_administrativo = Group.objects.create(name='Administrativo')

        # Usuarios
        self.user_supervisor = User.objects.create_user(username='super_test', password='password123')
        self.user_supervisor.groups.add(self.grupo_supervisor)

        self.user_administrativo = User.objects.create_user(username='adminis_test', password='password123')
        self.user_administrativo.groups.add(self.grupo_administrativo)

        # Zona
        self.zona = Zona.objects.create(
            nombre='La Serena Centro',
            destacado='Cercano a plaza de armas',
            nivel_demanda='Alta'
        )

        # Propiedad
        self.propiedad = Propiedad.objects.create(
            titulo='Casa Moderna en La Serena',
            tipo='Casa',
            precio='4.500 UF',
            habitaciones=3,
            banos=2,
            descripcion='Hermosa casa en sector residencial con excelente conectividad.',
            zona=self.zona
        )

    def test_inicio_carga(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)

    def test_lista_muestra_propiedades(self):
        response = self.client.get(reverse('propiedades:lista'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Casa Moderna en La Serena')

    def test_busqueda_propiedades_por_texto(self):
        response = self.client.get(reverse('propiedades:lista'), {'q': 'Moderna'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Casa Moderna en La Serena')

        response_vacio = self.client.get(reverse('propiedades:lista'), {'q': 'InexistenteXYZ'})
        self.assertContains(response_vacio, 'No se encontraron propiedades')

    def test_agregar_propiedad_valida(self):
        self.client.login(username='adminis_test', password='password123')
        data = {
            'titulo': 'Departamento Frente al Mar',
            'tipo': 'Departamento',
            'precio': '3.200 UF',
            'habitaciones': 2,
            'banos': 1,
            'descripcion': 'Vista panorámica al mar en Avenida del Mar.',
            'zona': self.zona.id
        }
        response = self.client.post(reverse('propiedades:agregar'), data, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(Propiedad.objects.filter(titulo='Departamento Frente al Mar').exists())

    def test_modificar_propiedad_por_supervisor(self):
        self.client.login(username='super_test', password='password123')
        data = {
            'titulo': 'Casa Moderna Renovada',
            'tipo': 'Casa',
            'precio': '4.800 UF',
            'habitaciones': 4,
            'banos': 3,
            'descripcion': 'Casa ampliada y remodelada recientemente.',
            'zona': self.zona.id
        }
        response = self.client.post(reverse('propiedades:editar', args=[self.propiedad.id]), data, follow=True)
        self.assertEqual(response.status_code, 200)
        self.propiedad.refresh_from_db()
        self.assertEqual(self.propiedad.titulo, 'Casa Moderna Renovada')
        self.assertEqual(self.propiedad.habitaciones, 4)

    def test_eliminar_propiedad_restringido_para_administrativo(self):
        # Un administrativo NO tiene permisos para eliminar propiedades
        self.client.login(username='adminis_test', password='password123')
        response = self.client.post(reverse('propiedades:eliminar', args=[self.propiedad.id]), follow=True)
        self.assertTrue(Propiedad.objects.filter(id=self.propiedad.id).exists())
        self.assertContains(response, 'Acceso denegado')

    def test_eliminar_propiedad_por_supervisor(self):
        self.client.login(username='super_test', password='password123')
        response = self.client.post(reverse('propiedades:eliminar', args=[self.propiedad.id]), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(Propiedad.objects.filter(id=self.propiedad.id).exists())
