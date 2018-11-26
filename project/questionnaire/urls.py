from django.urls import path
from . import views

urlpatterns = [
    path('api/questionnaire/', views.QuestionnaireListCreate.as_view()),
    path('getQuestionnaireList/', views.get_questionnaire_list),
    path('getQuestion/<str:questionnaire_id>/', views.get_next_question),
    path('answerQuestion', views.answer_question),
]