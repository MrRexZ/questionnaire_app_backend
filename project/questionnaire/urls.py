from django.urls import path
from . import views

urlpatterns = [
    path('api/questionnaire/', views.questionnaire_list_api.QuestionnaireListCreate.as_view()),
    path('getQuestionnaireList/', views.questionnaire_list_view.get_questionnaire_list),
    path('getQuestion/<str:questionnaire_id>/', views.questionnaire_list_view.get_next_question),
    path('answerQuestion', views.questionnaire_list_view.answer_question),
]