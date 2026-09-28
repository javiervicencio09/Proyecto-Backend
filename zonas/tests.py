from django.test import TestCase


class ListaZonasTests(TestCase):
	def test_lista_muestra_zonas(self):
		response = self.client.get('/zonas/')

		self.assertEqual(response.status_code, 200)
		self.assertContains(response, 'La Serena Centro')
