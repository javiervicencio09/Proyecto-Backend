from django.test import TestCase


class PaginasPropiedadesTests(TestCase):
	def test_inicio_carga(self):
		response = self.client.get('/')

		self.assertEqual(response.status_code, 200)
		self.assertContains(response, 'Portal Inmobiliario Coquimbo')

	def test_lista_muestra_propiedades(self):
		response = self.client.get('/propiedades/')

		self.assertEqual(response.status_code, 200)
		self.assertContains(response, 'Casa Moderna en La Serena')
