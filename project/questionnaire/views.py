from django.shortcuts import render
from rest_framework import generics
from .models import Questionnaire
from .serializers import QuestionnaireSerializers
import uuid
from django.http import HttpResponse
from django.core.cache import cache
from rest_framework.decorators import api_view
import logging
from django.core import serializers
import json
# Create your views here.

logger = logging.getLogger(__name__)


class QuestionnaireListCreate(generics.ListCreateAPIView):
    queryset = Questionnaire.objects.all()
    serializer_class = QuestionnaireSerializers


@api_view(['GET'])
def get_next_question(request, questionnaire_id):
    u_id = request.session['u_id']
    if (u_id is None):
        u_id = questionnaire_id + uuid.uuid4()
        cache[u_id] = ["q1", []]
    next_q_id = get_next_q_id(u_id)
    progress_list = get_progress_list(u_id)
    if (next_q_id is None):
        cache.delete(u_id)
        return log_result_complete(progress_list)
    else:
        return HttpResponse(get_question_and_answers(questionnaire_id, next_q_id), content_type='application/json')


def log_result_complete(progress_list):
    logger.info(progress_list)


def get_question_and_answers(questionnaire_id, q_id):
    questionnaire = Questionnaire.objects.get(id=questionnaire_id)
    question = questionnaire.questions[q_id]
    questions_json = serializers.serialize('json', question)
    return questions_json


def get_next_q_id(u_id):
    return cache[u_id][0]


def get_progress_list(u_id):
    return cache[u_id][1]


# Modify cache with next question id and alter progress string with answer selected by ID passed.
@api_view(['POST'])
def answer_question(request):
    body = json.load(request.body)
    a_id = body['a_id']
    questionnaire_id = body['questionnaire_id']
    u_id = request.session['u_id']
    cur_q_id = get_next_q_id(u_id)
    answer_data = get_answer_data(questionnaire_id, cur_q_id, a_id)
    next_q_id = answer_data['next_q_id']
    answer_text = answer_data['ans_name']
    update_next_question_data(u_id, next_q_id, answer_text)


def update_next_question_data(u_id, next_q_id, answer_text):
    update_progress_list(u_id, answer_text)
    set_next_q_id(u_id, next_q_id)

def set_next_q_id(u_id, next_q_id):
    cache[u_id][0] = next_q_id


def update_progress_list(u_id, answer_text):
    cache[u_id][1] +=  answer_text + '\n'


def get_answer_data(questionnaire_id, q_id, a_id):
    questionnaire = Questionnaire.objects.get(id=questionnaire_id)
    question = questionnaire.questions[q_id]
    answers = question['answers']
    for answer in answers:
        if answer['ans_id'] is a_id:
            return answer
    return None
