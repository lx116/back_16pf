import pandas as pd
from django.db.models import F
from rest_framework.generics import ListAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser
from .models import Respondent, PersonalityFactors, Categorization
from .serializer import RespondentSerializer, PersonalityFactorsSerializer, CategorizationSerializer


class ExcelUploadView(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request):
        file = request.FILES['file']

        if not file:
            return Response({'error': 'No FIle Provided'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            excel_data = pd.ExcelFile(file)

            required_columns = ['name', 'age', 'gender',
                                'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H',
                                'I', 'L', 'M', 'N', 'O', 'Q1', 'Q2', 'Q3', 'Q4',
                                'An', 'Ex', 'So', 'In', 'Ob', 'Cr', 'Ne', 'Ps', 'Li', 'Ac']

            missing_columns = [col for col in required_columns if col not in excel_data.columns]

            if missing_columns:
                return Response({"error": f"Missing columns in Excel: {missing_columns}"},
                                status=status.HTTP_400_BAD_REQUEST)

            current_count = Respondent.objects.count()
            new_counter = current_count + 1

            for _, row in excel_data.iterrows():
                name = row['name'] if pd.notnull(row['name']) else f"Estudiante {new_counter}"

                if pd.isnull(row['name']):
                    new_counter += 1

                respondent, _ = Respondent.objects.update_or_create(
                    name=name,
                    defaults={'age': row['age'], 'gender': row['gender']}
                )

                PersonalityFactors.objects.update_or_create(
                    respondent=respondent,
                    defaults={col: row[col] for col in required_columns[3:20]}  # Columnas de A a Q4
                )

                Categorization.objects.update_or_create(
                    respondent=respondent,
                    defaults={col: row[col] for col in required_columns[20:]}  # Columnas de An a Ac
                )

            return Response({"message": "Excel data processed successfully"}, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({'error': f'File Not Found {e}'}, status=status.HTTP_400_BAD_REQUEST)


class RespondentListView(ListAPIView):
    queryset = Respondent.objects.all()
    serializer_class = RespondentSerializer


class PersonalityFactorsByRespondentView(ListAPIView):
    serializer_class = PersonalityFactorsSerializer

    def get_queryset(self):
        respondent_id = self.kwargs['respondent_id']
        return PersonalityFactors.objects.filter(respondent_id=respondent_id)


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
        valid_factors = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'L', 'M', 'N', 'O', 'Q1', 'Q2', 'Q3', 'Q4']
        if factor1 not in valid_factors or factor2 not in valid_factors:
            return Response(
                {"error": f"Invalid factors. Valid factors are: {', '.join(valid_factors)}."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Filtrar y recuperar los valores de los factores
        factors = PersonalityFactors.objects.values(
            respondent_id=F('respondent_id'),  # Para incluir el ID del Respondent
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
    Vista para recuperar valores de dos categorías específicas elegidas por el usuario.
    """
    def get(self, request, *args, **kwargs):
        # Recuperar parámetros de consulta
        category1 = request.query_params.get('category1')
        category2 = request.query_params.get('category2')
        respondent_id = request.query_params.get('respondent_id')  # Nuevo parámetro opcional

        # Validar que ambas categorías se hayan proporcionado
        if not category1 or not category2:
            return Response(
                {"error": "Both 'category1' and 'category2' query parameters are required."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Validar que las categorías existen en el modelo
        valid_categories = ['An', 'Ex', 'So', 'In', 'Ob', 'Cr', 'Ne', 'Ps', 'Li', 'Ac']
        if category1 not in valid_categories or category2 not in valid_categories:
            return Response(
                {"error": f"Invalid categories. Valid categories are: {', '.join(valid_categories)}."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Construir consulta base
        query = Categorization.objects.values(
            respondent_id=F('respondent_id'),
            category1=F(category1),
            category2=F(category2)
        )

        # Aplicar filtro por respondent_id si se proporciona
        if respondent_id:
            query = query.filter(respondent_id=respondent_id)

        return Response(query, status=status.HTTP_200_OK)

