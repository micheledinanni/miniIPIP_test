from django.urls import path
from . import views

app_name='myapp'
urlpatterns = [
    path('',views.begin,name='begin'),
    path('start/',views.index,name='index'),
    path('<int:question_id>/',views.detail,name='detail'),
    path('<int:question_id>/vote/',views.vote,name='vote'),
    path('evaluation/',views.evaluate,name='evaluation'),
]