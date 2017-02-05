# django_first_test
After installing Django. You need to install the following packages:

Requirements:
Celery:
  $ pip install celery

Redis:
  $ wget http://download.redis.io/releases/redis-3.2.7.tar.gz
  $ tar xzf redis-3.2.7.tar.gz
  $ cd redis-3.2.7
  $ make
 
  To test that redis works perfectly:
  $ redis-server
  $ redis-cli ping
  redis should reply with: PONG

Usage:
First you should fire redis server:
  $ redis-server

Then you should fire celery:
  $ celery -A mysite worker -l info
  this command is executed in upper mysite dir(not the app in the mysite dir).
  celery will be prepared for new tasks.

finally execute:
  $ python manage.py runserver

go to http://localhost:8000/init_work
refresh to see the progress made by the worker.

more info:
https://realpython.com/blog/python/asynchronous-tasks-with-django-and-celery/
https://www.digitalocean.com/community/tutorials/how-to-use-celery-with-rabbitmq-to-queue-tasks-on-an-ubuntu-vps
http://stackoverflow.com/questions/7380373/django-celery-progress-bar
