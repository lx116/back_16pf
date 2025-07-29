import pandas as pd
from django.db.models import F
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser
from .models import Respondent, PersonalityFactors, Categorization
from .serializer import RespondentSerializer, PersonalityFactorsSerializer, CategorizationSerializer


class ExcelUploadView(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request):
        file = request.FILES.get('file')

        if not file:
            return Response({'error': 'No File Provided'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Leer el archivo Excel
            excel_data = pd.read_excel(file)

            # Columnas requeridas
            personality_columns = [
                'A', 'B', 'C', 'E', 'F', 'G', 'H',
                'I', 'L', 'M', 'N', 'O', 'Q1', 'Q2', 'Q3', 'Q4'
            ]
            categorization_columns = ['An', 'Ex', 'So', 'In', 'Ob', 'Cr', 'Ne', 'Ps', 'Li', 'Ac']
            required_columns = ['name', 'age', 'gender'] + personality_columns + categorization_columns

            # Verificar columnas faltantes
            missing_columns = [col for col in required_columns if col not in excel_data.columns]
            if missing_columns:
                return Response(
                    {"error": f"Missing columns in Excel: {', '.join(missing_columns)}"},
                    status=status.HTTP_400_BAD_REQUEST
                )

            # Contador para nombres automáticos
            current_count = Respondent.objects.count()
            new_counter = current_count + 1

            # Mapeo para género
            gender_map = {'masculino': 'M', 'femenino': 'F'}

            # Procesar filas del Excel
            for _, row in excel_data.iterrows():
                # Validar datos de la fila
                name = row['name'] if pd.notnull(row['name']) else f"Estudiante {new_counter}"
                if pd.isnull(row['name']):
                    new_counter += 1

                gender = gender_map.get(row['gender'].strip().lower(), row['gender'])  # Convertir género

                respondent, _ = Respondent.objects.update_or_create(
                    name=name,
                    defaults={'age': row['age'], 'gender': gender}
                )

                # Crear o actualizar PersonalityFactors
                PersonalityFactors.objects.update_or_create(
                    respondent=respondent,
                    defaults={col: row[col] for col in personality_columns if col in row}
                )

                # Crear o actualizar Categorization
                Categorization.objects.update_or_create(
                    respondent=respondent,
                    defaults={col: row[col] for col in categorization_columns if col in row}
                )

            return Response({"message": "Excel data processed successfully"}, status=status.HTTP_201_CREATED)

        except ValueError as e:
            return Response({'error': f'Invalid Excel File: {e}'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': f'Unexpected error: {e}'}, status=status.HTTP_400_BAD_REQUEST)

class RespondentListView(ListAPIView):
    queryset = Respondent.objects.all()
    serializer_class = RespondentSerializer


class RespondentDetailView(RetrieveAPIView):
    queryset = Respondent.objects.all()
    serializer_class = RespondentSerializer

class PersonalityFactorsByRespondentView(ListAPIView):
    serializer_class = PersonalityFactorsSerializer

    def get_queryset(self):
        respondent_id = self.kwargs['respondent_id']
        queryset = PersonalityFactors.objects.filter(respondent_id=respondent_id)
        print(f"Queryset for respondent_id {respondent_id}: {queryset}")
        return queryset


class PersonalityFactorsFilterView(APIView):
    """
    Vista para recuperar valores de dos factores de personalidad específicos elegidos por el usuario.
    """
    def get(self, request, *args, **kwargs):
        # Recuperar parámetros de consulta
        factor1 = request.query_params.get('factor1')
        factor2 = request.query_params.get('factor2')

        # Validar que ambos factores se hayan proporcionado
        if not factor1 or not factor2:
            return Response(
                {"error": "Both 'factor1' and 'factor2' query parameters are required."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Validar que los factores existen en el modelo
        valid_factors = ['A', 'B', 'C', 'E', 'F', 'G', 'H', 'I', 'L', 'M', 'N', 'O', 'Q1', 'Q2', 'Q3', 'Q4']
        if factor1 not in valid_factors or factor2 not in valid_factors:
            return Response(
                {"error": f"Invalid factors. Valid factors are: {', '.join(valid_factors)}."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Recuperar factores con IDs y nombres de los respondientes
        factors = PersonalityFactors.objects.select_related('respondent').values(
            annotated_respondent_id=F('respondent__id'),  # ID del respondiente
            respondent_name=F('respondent__name'),  # Nombre del respondiente
            factor1=F(factor1),
            factor2=F(factor2)
        )

        return Response(factors, status=status.HTTP_200_OK)




class CategorizationByRespondentView(ListAPIView):
    serializer_class = CategorizationSerializer

    def get_queryset(self):
        respondent_id = self.kwargs['respondent_id']
        return Categorization.objects.filter(respondent_id=respondent_id)


class CategorizationFilterView(APIView):
    """
    Vista para filtrar categorías específicas elegidas por el usuario.
    """
    def get(self, request, *args, **kwargs):
        # Recuperar parámetros de consulta
        category1 = request.query_params.get('category1')
        category2 = request.query_params.get('category2')

        # Validar que ambas categorías se hayan proporcionado
        if not category1 or not category2:
            return Response(
                {"error": "Both 'category1' and 'category2' query parameters are required."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Validar que las categorías existen en el modelo
        valid_categories = ['An', 'Ex', 'So', 'In', 'Ob', 'Cr', 'Ne', 'Ps', 'Li', 'Ac']  # Agregar las categorías válidas
        if category1 not in valid_categories or category2 not in valid_categories:
            return Response(
                {"error": f"Invalid categories. Valid categories are: {', '.join(valid_categories)}."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Cambiar el nombre de la anotación para evitar conflicto
        query = Categorization.objects.values(
            annotated_respondent_id=F('respondent__id'),  # ID del respondiente
            respondent_name=F('respondent__name'),  # Nombre del respondiente
            category1=F(category1),
            category2=F(category2)
        )

        return Response(query, status=status.HTTP_200_OK)


