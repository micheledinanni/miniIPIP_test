
from django.shortcuts import render, get_object_or_404
from django.urls import reverse

from .models import Question, Choice,People
from django.db.models import Avg
from django.http import HttpResponse, HttpResponseRedirect


# Create your views here.

def begin(request):
    return render(request,'myapp/begin.html')


def index(request):
    question_list = Question.objects.all()
    context = {'question_list': question_list}
    return render(request, 'myapp/index.html', context)


def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'myapp/detail.html', {'question': question})


def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        return render(request, 'myapp/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
         Question.objects.filter(pk=question_id).update(score=selected_choice.punteggio)
    return HttpResponseRedirect(reverse('myapp:detail', args=(question.id,)))


def evaluate(request):
    if(Question.objects.filter(score=0)):
      return HttpResponse("You haven't complete the test. Please come back and ckeck to get the final result.")
    else:
        extraversion = Question.objects.filter(cat='E').aggregate(mean=Avg('score'))['mean']
        agreeableness = Question.objects.filter(cat='A').aggregate(mean=Avg('score'))['mean']
        openness = Question.objects.filter(cat='O').aggregate(mean=Avg('score'))['mean']
        coscientiousness = Question.objects.filter(cat='C').aggregate(mean=Avg('score'))['mean']
        neuroticism = Question.objects.filter(cat='N').aggregate(mean=Avg('score'))['mean']
        q = People(extraversion=extraversion,agreeableness=agreeableness,
                   openness=openness,coscientiousness=coscientiousness,neuroticism=neuroticism)
        q.save()
    return render(request,'myapp/evaluation.html',{'extraversion':q.extraversion,
                                                   'agreeableness':q.agreeableness,
                                                   'openness':q.openness,
                                                   'coscientiousness':q.coscientiousness,
                                                   'neuroticism':q.neuroticism})
