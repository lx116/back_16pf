from django.urls import path
from .views import ExcelUploadView, RespondentListView, PersonalityFactorsFilterView, \
    PersonalityFactorsByRespondentView, CategorizationFilterView, CategorizationByRespondentView, RespondentDetailView

urlpatterns = [
    path('upload-excel/', ExcelUploadView.as_view(), name='upload-excel'),
    path('respontents/', RespondentListView.as_view(), name='respontents'),
    path('respondents/<int:pk>/', RespondentDetailView.as_view(), name='respondent-detail'),
    path('personality-factors-filter/', PersonalityFactorsFilterView.as_view(), name='personality-factors-filter'),
    path('personality-factors/<int:respondent_id>/', PersonalityFactorsByRespondentView.as_view(),
         name='personality-factors'),
    path('categorization-filter/', CategorizationFilterView.as_view(), name='categorization'),
    path('categorization/<int:respondent_id>/', CategorizationByRespondentView.as_view(), name='categorization'),

]
