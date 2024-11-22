from django.contrib import admin
from .models import Respondent, PersonalityFactors, Categorization

# Registra el modelo Respondent con el administrador para mostrar el nombre
@admin.register(Respondent)
class RespondentAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'age', 'gender')  # Muestra el ID y los detalles básicos
    search_fields = ('name',)  # Permite buscar por nombre

# Registra el modelo PersonalityFactors con el administrador para mostrar el ID del respondent y su nombre
@admin.register(PersonalityFactors)
class PersonalityFactorsAdmin(admin.ModelAdmin):
    list_display = ('id', 'respondent_id', 'respondent_name')  # Muestra el ID del PersonalityFactors y el nombre del respondent
    search_fields = ('respondent__name',)  # Permite buscar por nombre del respondent

    def respondent_name(self, obj):
        return obj.respondent.name  # Retorna el nombre del respondent

    respondent_name.admin_order_field = 'respondent__name'  # Habilita la ordenación por el nombre del respondent
    respondent_name.short_description = 'Respondent Name'  # Etiqueta personalizada para la columna

# Registra el modelo Categorization con el administrador para mostrar el ID del respondent y su nombre
@admin.register(Categorization)
class CategorizationAdmin(admin.ModelAdmin):
    list_display = ('id', 'respondent_id', 'respondent_name')  # Muestra el ID del Categorization y el nombre del respondent
    search_fields = ('respondent__name',)  # Permite buscar por nombre del respondent

    def respondent_name(self, obj):
        return obj.respondent.name  # Retorna el nombre del respondent

    respondent_name.admin_order_field = 'respondent__name'  # Habilita la ordenación por el nombre del respondent
    respondent_name.short_description = 'Respondent Name'  # Etiqueta personalizada para la columna
