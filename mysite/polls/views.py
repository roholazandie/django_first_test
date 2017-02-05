from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
import time
from django.views.decorators.csrf import csrf_exempt
from tasks import do_work
from time import sleep
from celery.result import AsyncResult
import json
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse

def index(request):
    latest_question_list = ['this',
     'is',
     'an',
     'example']
    template = loader.get_template('polls/index.html')
    context = {'latest_question_list': latest_question_list}
    return HttpResponse(template.render(context, request))


def vote(request):
    try:
        selected_choice = request.GET['choice']
        template = loader.get_template('polls/detail.html')
    except KeyError:
        selected_choice = 'Nothing'
        template = loader.get_template('polls/detail.html')
        context = {'output': selected_choice}

    return HttpResponse(template.render(context, request))


def poll_state(request):
    """ A view to report the progress to the user """
    if 'job' in request.GET:
        job_id = request.GET['job']
    else:
        return HttpResponse('No job id given.')
    job = AsyncResult(job_id)
    data = job.result or job.state
    return HttpResponse(json.dumps(data), content_type='application/json')


def init_work(request):
    """ A view to start a background job and redirect to the status page """
    job = do_work.delay()
    return HttpResponseRedirect(reverse('poll_state') + '?job=' + job.id)