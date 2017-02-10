from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
import time
from django.views.decorators.csrf import csrf_exempt
from tasks import do_work
from time import sleep
from celery.result import AsyncResult
from .forms import UserForm
import json
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
import logging

logger = logging.getLogger(__name__)


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
    data = 'Fail'
    if request.is_ajax():
        if 'job_id' in request.POST.keys() and request.POST['job_id']:
            job_id = request.POST['job_id']
            job = AsyncResult(job_id)
            data = job.result or job.state
        else:
            data = 'No job_id in the request'
    else:
        data = 'This is not an ajax request'

    json_data = json.dumps(data)
    return HttpResponse(json_data, content_type='application/json')

'''
def init_work(request):
    """ A view to start a background job and redirect to the status page """
    if request.method == "POST":
        return HttpResponse("message")
    if 'job_id' in request.GET:
        job_id = request.GET['job_id']
        job = AsyncResult(job_id)
        data = job.result or job.state
        context = {
            'data': data,
            'job_id': job_id,
        }
        return render(request, "show_t.html", context)
    elif 'n' in request.GET:
        n = request.GET['n']
        job = do_work.delay()
        # context = {
        #    'job_id': job.id
        # }
        return HttpResponseRedirect(reverse('init_work') + '?job_id=' + job.id)
    else:
        form = UserForm()
        context = {
            'form': form,
        }
        logger.info("form")
        return render(request, "show_t.html", context)
'''

def create_post(request):
    """
    An ajax form that first startup by GET and
    after the submission the job_id gets a value
    and the scripts then appears
    """
    if request.method == 'POST':
        n = request.POST.get('n')

        form = UserForm()
        job = do_work.delay()
        context = {
            'form': form,
            'job_id': job.id,
            'n_value': n,
        }
        template = loader.get_template('polls/show_t.html')
        return HttpResponse(template.render(context, request))
    else:
        form = UserForm()
        context = {
            'form': form,
        }
        template = loader.get_template('polls/show_t.html')
        return HttpResponse(template.render(context, request))
