from celery import Celery
from celery import task, current_task
import time
app = Celery('tasks', backend='redis', broker='redis://localhost')

@app.task
def do_work():
    """ Get some rest, asynchronously, and update the state all the time """
    for i in range(100):
        time.sleep(0.1)
        current_task.update_state(state='PROGRESS', meta={'current': i, 'total': 100})