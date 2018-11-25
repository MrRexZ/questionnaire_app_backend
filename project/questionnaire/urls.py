from django.urls import path
from . import views

urlpatterns = [
    path('api/questionnaire/', views.QuestionnaireListCreate.as_view()),
]