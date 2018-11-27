from __future__ import absolute_import
from rest_framework import generics, mixins
from questionnaire.serializers import QuestionnaireSerializers
from questionnaire.models import Questionnaire


class QuestionnaireListCreate(generics.ListCreateAPIView, mixins.DestroyModelMixin):
    queryset = Questionnaire.objects.all()
    serializer_class = QuestionnaireSerializers

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


