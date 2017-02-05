from django.conf.urls import url
from . import views
urlpatterns = [url('^$', views.init_work, name='init_work'),
               url('^poll_state$', views.poll_state, name='poll_state')]