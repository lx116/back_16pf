from rest_framework.test import APITestCase
from rest_framework import status
from django.core.files.uploadedfile import SimpleUploadedFile
from ..models import Respondent, PersonalityFactors, Categorization
import pandas as pd
import io


class ExcelUploadViewTests(APITestCase):

    def setUp(self):
        # Crear un archivo Excel simulado
        data = {
            'name': ['John Doe'],
            'age': [25],
            'gender': ['Male'],
            'A': [1], 'B': [2], 'C': [3], 'D': [4], 'E': [5], 'F': [6], 'G': [7], 'H': [8],
            'I': [9], 'L': [10], 'M': [11], 'N': [12], 'O': [13], 'Q1': [14], 'Q2': [15], 'Q3': [16], 'Q4': [17],
            'An': [18], 'Ex': [19], 'So': [20], 'In': [21], 'Ob': [22], 'Cr': [23], 'Ne': [24], 'Ps': [25], 'Li': [26], 'Ac': [27]
        }
        self.df = pd.DataFrame(data)
        excel_buffer = io.BytesIO()
        self.df.to_excel(excel_buffer, index=False)
        self.excel_file = SimpleUploadedFile("test.xlsx", excel_buffer.getvalue(), content_type="application/vnd.ms-excel")

    def test_valid_excel_upload(self):
        response = self.client.post('/api/upload-excel/', {'file': self.excel_file}, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Respondent.objects.count(), 1)
        self.assertEqual(PersonalityFactors.objects.count(), 1)
        self.assertEqual(Categorization.objects.count(), 1)

    def test_missing_file(self):
        response = self.client.post('/api/upload-excel/', {}, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('No File Provided', response.data['error'])


    def test_missing_columns(self):
        invalid_data = {
            'name': ['John Doe'],
            'age': [25],
        }
        df = pd.DataFrame(invalid_data)
        buffer = io.BytesIO()
        df.to_excel(buffer, index=False)
        invalid_file = SimpleUploadedFile("test_invalid.xlsx", buffer.getvalue(), content_type="application/vnd.ms-excel")
        response = self.client.post('/api/upload-excel/', {'file': invalid_file}, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('Missing columns in Excel', response.data['error'])


class PersonalityFactorsFilterViewTests(APITestCase):

    def setUp(self):
        # Crear un respondiente y factores asociados
        self.respondent = Respondent.objects.create(name="John Doe", age=25, gender="Male")
        PersonalityFactors.objects.create(respondent=self.respondent, A=1, B=2, C=3, E=4)

        self.valid_url = '/api/personality-factors-filter/'

    def test_valid_factors(self):
        # Caso feliz: factores válidos
        response = self.client.get(self.valid_url, {'factor1': 'A', 'factor2': 'B'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(len(response.data) > 0)  # Hay resultados
        self.assertEqual(response.data[0]['factor1'], 1)
        self.assertEqual(response.data[0]['factor2'], 2)

    def test_missing_factors(self):
        # Faltan factores
        response = self.client.get(self.valid_url, {'factor1': 'A'})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("Both 'factor1' and 'factor2' query parameters are required", response.data['error'])

    def test_invalid_factors(self):
        # Factores inválidos
        response = self.client.get(self.valid_url, {'factor1': 'X', 'factor2': 'Y'})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("Invalid factors", response.data['error'])

    def test_no_query_params(self):
        # Sin parámetros de consulta
        response = self.client.get(self.valid_url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("Both 'factor1' and 'factor2' query parameters are required", response.data['error'])

    def test_one_valid_one_invalid_factor(self):
        # Un factor válido y uno inválido
        response = self.client.get(self.valid_url, {'factor1': 'A', 'factor2': 'Z'})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("Invalid factors", response.data['error'])

    def test_no_results_for_valid_factors(self):
        # Factores válidos pero sin datos asociados
        PersonalityFactors.objects.all().delete()  # Borrar datos
        response = self.client.get(self.valid_url, {'factor1': 'A', 'factor2': 'B'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)  # Sin resultados

class CategorizationFilterViewTests(APITestCase):

    def setUp(self):
        respondent = Respondent.objects.create(name="John Doe", age=25, gender="Male")
        Categorization.objects.create(respondent=respondent, An=1, Ex=2, So=3)

    def test_valid_categories(self):
        response = self.client.get('/api/categorization-filter/', {'category1': 'An', 'category2': 'Ex'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('category1', response.data[0])
        self.assertIn('category2', response.data[0])

    def test_missing_categories(self):
        response = self.client.get('/api/categorization-filter/', {'category1': 'An'})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("Both 'category1' and 'category2' query parameters are required", response.data['error'])

    def test_invalid_categories(self):
        response = self.client.get('/api/categorization-filter/', {'category1': 'X', 'category2': 'Ex'})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("Invalid categories", response.data['error'])
