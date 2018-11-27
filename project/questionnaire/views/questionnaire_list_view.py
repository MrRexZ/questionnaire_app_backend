from __future__ import absolute_import
from django.http import HttpResponse
from rest_framework.decorators import api_view
import uuid
from .base_views import *

from django.core.cache import cache


@api_view(['GET'])
def get_questionnaire_list(request):
    questionnaire_ids = Questionnaire.objects.all()
    return HttpResponse(json.dumps(list(questionnaire_ids.values("id", "questionnaire_name"))),
                        content_type='application/json')


@api_view(['GET'])
def get_next_question(request, questionnaire_id):
    if 'u_id' not in request.session or not_cached_yet(request.session):
        u_id = questionnaire_id + str(uuid.uuid4())
        cache.set(u_id, ["q1", []])
        request.session['u_id'] = u_id
    else:
        u_id = request.session['u_id']
    next_q_id = get_next_q_id(u_id)
    if (next_q_id is None):
        progress_list = get_progress_list(u_id)
        cache.delete(u_id)
        log_result_complete(progress_list)
        res = {'complete': True, 'dialog': progress_list}
        return HttpResponse(json.dumps(res), content_type='application/json')
    else:
        return HttpResponse(get_question_and_answers(questionnaire_id, next_q_id), content_type='application/json')


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
