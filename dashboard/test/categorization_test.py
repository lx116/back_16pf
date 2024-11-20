from rest_framework.test import APITestCase
from rest_framework import status
from ..models import Categorization, Respondent
from django.urls import reverse


class CategorizationFilterViewTest(APITestCase):

    def setUp(self):
        # Crear Respondents de ejemplo
        self.respondent1 = Respondent.objects.create(name="Estudiante 1", age=25, gender="M")
        self.respondent2 = Respondent.objects.create(name="Estudiante 2", age=30, gender="F")

        # Crear Categorization para esos Respondents
        Categorization.objects.create(respondent=self.respondent1, An=1.5, Ex=2.5, So=3.5)
        Categorization.objects.create(respondent=self.respondent2, An=4.5, Ex=5.5, So=6.5)

        self.url = reverse('categorization-filter')

    def test_get_categorization_success(self):
        # Test para obtener las categorías An y Ex para todos los Respondents
        response = self.client.get(self.url, {'category1': 'An', 'category2': 'Ex'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.data[0]['category1'], 1.5)
        self.assertEqual(response.data[1]['category2'], 5.5)

    def test_get_categorization_invalid_category(self):
        # Test para una categoría inválida
        response = self.client.get(self.url, {'category1': 'Z', 'category2': 'Ex'})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('Invalid categories', response.data['error'])

    def test_get_categorization_missing_param(self):
        # Test para cuando faltan parámetros
        response = self.client.get(self.url, {'category1': 'An'})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('Both \'category1\' and \'category2\' query parameters are required.', response.data['error'])

    def test_get_categorization_by_respondent(self):
        # Test para obtener las categorías An y Ex de un Respondent específico
        response = self.client.get(self.url,
                                   {'category1': 'An', 'category2': 'Ex', 'respondent_id': self.respondent1.id})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['respondent_id'], self.respondent1.id)
