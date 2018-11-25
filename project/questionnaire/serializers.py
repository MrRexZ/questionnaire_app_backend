from rest_framework import serializers
from .models import Questionnaire


class QuestionnaireSerializers(serializers.ModelSerializer):
    class Meta:
        model = Questionnaire
        fields = '__all__'
