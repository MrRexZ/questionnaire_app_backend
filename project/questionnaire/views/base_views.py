from __future__ import absolute_import
from .base_views import *
import logging
from questionnaire.models import Questionnaire
import json
from django.core.cache import cache

logger = logging.getLogger(__name__)

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
