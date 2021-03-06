from django.db import models
from django.contrib.postgres.fields import JSONField


class Questionnaire(models.Model):
    id = models.CharField(max_length=255, primary_key=True)
    questionnaire_name = models.CharField(max_length=255)
    questions = JSONField()
