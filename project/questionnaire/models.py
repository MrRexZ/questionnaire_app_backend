from django.db import models
from django.contrib.postgres.fields import JSONField
# Create your models here.

class Questionnaire(models.Model):
    id = models.CharField(max_length=255, primary_key=True)
    questions = JSONField()
