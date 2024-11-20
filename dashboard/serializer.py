from rest_framework import serializers
from .models import Respondent, PersonalityFactors, Categorization

class RespondentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Respondent
        fields = ['id', 'name', 'age', 'gender']

class PersonalityFactorsSerializer(serializers.ModelSerializer):
    respondent = serializers.StringRelatedField()  # Puedes usar esto para mostrar el nombre del respondente en lugar de su ID
    respondent_id = serializers.PrimaryKeyRelatedField(queryset=Respondent.objects.all(), source='respondent', write_only=True)

    class Meta:
        model = PersonalityFactors
        fields = [
            'id', 'respondent', 'respondent_id',
            'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H',
            'I', 'L', 'M', 'N', 'O', 'Q1', 'Q2', 'Q3', 'Q4'
        ]

class CategorizationSerializer(serializers.ModelSerializer):
    respondent = serializers.StringRelatedField()  # También muestra el nombre del respondente
    respondent_id = serializers.PrimaryKeyRelatedField(queryset=Respondent.objects.all(), source='respondent', write_only=True)

    class Meta:
        model = Categorization
        fields = [
            'id', 'respondent', 'respondent_id',
            'An', 'Ex', 'So', 'In', 'Ob',
            'Cr', 'Ne', 'Ps', 'Li', 'Ac'
        ]
