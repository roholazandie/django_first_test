from celery import Celery
from celery import task, current_task
import time
import numpy as np
app = Celery('tasks', backend='redis', broker='redis://localhost')

@app.task(bind=True)
def do_work(n,t):
    """ Get some rest, asynchronously, and update the state all the time """
    for i in range(100):
        time.sleep(0.1)

        current_task.update_state(state='PROGRESS', meta={'process_percent': i, 'total': 100})