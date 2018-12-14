from django.urls import path
from django.views.generic import TemplateView

from . import views
from django.conf.urls import url

app_name='myapp'
urlpatterns = [
    url(r'^(?:id=(?P<id>\w+)/)?$',views.index,name='index'),
    url(r'^test(?:id=(?P<id>\w+)/)?$',views.test,name='test'),
    url(r'^vote(?:id=(?P<id>\w+))/(?P<question_id>\d+)/(?P<page>\d+)?$',views.vote,name='vote'),
]