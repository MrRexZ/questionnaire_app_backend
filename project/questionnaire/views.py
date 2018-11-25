from django.shortcuts import render
from rest_framework import generics
from .models import Questionnaire
from .serializers import QuestionnaireSerializers
# Create your views here.

class QuestionnaireListCreate(generics.ListCreateAPIView):
    queryset = Questionnaire.objects.all()
    serializer_class = QuestionnaireSerializers