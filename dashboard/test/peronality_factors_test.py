from rest_framework.test import APITestCase
from rest_framework import status
from ..models import Respondent, PersonalityFactors
from django.urls import reverse


class PersonalityFactorsFilterViewTest(APITestCase):

    def setUp(self):
        # Crear Respondents de ejemplo
        self.respondent1 = Respondent.objects.create(name="Estudiante 1", age=25, gender="M")
        self.respondent2 = Respondent.objects.create(name="Estudiante 2", age=30, gender="F")

        # Crear PersonalityFactors para esos Respondents
        PersonalityFactors.objects.create(respondent=self.respondent1, A=1.5, B=2.5, C=3.5)
        PersonalityFactors.objects.create(respondent=self.respondent2, A=4.5, B=5.5, C=6.5)

        self.url = reverse('personality-factors-filter')

    def test_get_personality_factors_success(self):
        # Test para obtener los factores A y B para todos los Respondents
        response = self.client.get(self.url, {'factor1': 'A', 'factor2': 'B'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.data[0]['factor1'], 1.5)
        self.assertEqual(response.data[1]['factor2'], 5.5)

    def test_get_personality_factors_invalid_factor(self):
        # Test para un factor inválido
        response = self.client.get(self.url, {'factor1': 'X', 'factor2': 'B'})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('Invalid factors', response.data['error'])

    def test_get_personality_factors_missing_param(self):
        # Test para cuando faltan parámetros
        response = self.client.get(self.url, {'factor1': 'A'})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('Both \'factor1\' and \'factor2\' query parameters are required.', response.data['error'])

    def test_get_personality_factors_by_respondent(self):
        # Test para obtener los factores A y B de un Respondent específico
        response = self.client.get(self.url, {'factor1': 'A', 'factor2': 'B', 'respondent_id': self.respondent1.id})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['respondent_id'], self.respondent1.id)

