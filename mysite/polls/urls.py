from django.conf.urls import url
from . import views
urlpatterns = [url('^$', views.create_post, name='create_post'),
               url('^poll_state$', views.poll_state, name='poll_state')]