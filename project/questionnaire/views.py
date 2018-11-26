from django.shortcuts import render
from rest_framework import generics, mixins
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


class QuestionnaireListCreate(generics.ListCreateAPIView, mixins.DestroyModelMixin):
    queryset = Questionnaire.objects.all()
    serializer_class = QuestionnaireSerializers

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)

@api_view(['GET'])
def get_questionnaire_list(request):
    questionnaire_ids = Questionnaire.objects.all()
    return HttpResponse(json.dumps(list(questionnaire_ids.values_list("id", flat=True))), content_type='application/json')

@api_view(['GET'])
def get_next_question(request, questionnaire_id):
    if 'u_id' not in request.session or not_cached_yet(request.session):
        u_id = questionnaire_id + str(uuid.uuid4())
        cache.set(u_id,["q1", []])
        request.session['u_id'] = u_id
    else:
        u_id = request.session['u_id']
    next_q_id = get_next_q_id(u_id)
    if (next_q_id is None):
        progress_list = get_progress_list(u_id)
        cache.delete(u_id)
        log_result_complete(progress_list)
        return HttpResponse()
    else:
        return HttpResponse(get_question_and_answers(questionnaire_id, next_q_id), content_type='application/json')


def not_cached_yet(session):
    return cache.get(session['u_id']) is None

def log_result_complete(progress_list):
    logger.info(progress_list)


def get_question_and_answers(questionnaire_id, q_id):
    question = get_question(questionnaire_id, q_id)
    questions_json = json.dumps(question)
    return questions_json


def get_question(questionnaire_id, q_id):
    questionnaire = Questionnaire.objects.get(id=questionnaire_id)
    question = questionnaire.questions[q_id]
    return question


def get_next_q_id(u_id):
    return cache.get(u_id)[0]


def get_progress_list(u_id):
    return cache.get(u_id)[1]


# Modify cache with next question id and alter progress string with answer selected by ID passed.
@api_view(['POST'])
def answer_question(request):
    body = json.loads(request.body)
    a_id = body['a_id']
    questionnaire_id = body['questionnaire_id']
    u_id = request.session['u_id']
    cur_q_id = get_next_q_id(u_id)
    answer_data = get_answer_data(questionnaire_id, cur_q_id, a_id)
    next_q_id = answer_data.get('next_q_id')
    answer_text = answer_data.get('ans_name')
    remark = answer_data.get('remark')
    update_next_question_data(u_id, questionnaire_id, cur_q_id, next_q_id, answer_text, remark)
    return HttpResponse()


def update_next_question_data(u_id, questionnaire_id, cur_q_id, next_q_id, answer_text, remark):
    update_progress_list(u_id, get_question(questionnaire_id, cur_q_id)['q_name'])
    update_progress_list(u_id, answer_text)
    if remark is not None:
        update_progress_list(u_id, remark)
    set_next_q_id(u_id, next_q_id)


def set_next_q_id(u_id, next_q_id):
    cache.set(u_id, [next_q_id, get_progress_list(u_id)])


def update_progress_list(u_id, answer_text):
    existing_progress_list = get_progress_list(u_id)
    existing_progress_list.append(answer_text)
    cache.set(u_id, [get_next_q_id(u_id), existing_progress_list])


def get_answer_data(questionnaire_id, q_id, a_id):
    questionnaire = Questionnaire.objects.get(id=questionnaire_id)
    question = questionnaire.questions[q_id]
    answers = question['answers']
    for answer in answers:
        if answer['ans_id'] == a_id:
            return answer
    return None
