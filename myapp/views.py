from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from .models import Question, Choice,People,PeopleQuestions
from django.db.models import Avg

# Create your views here.

def index (request,id):
    user = request.GET.get('id','')
    return render(request,'myapp/index.html',{'user':user})

def test(request,id):
    user = request.GET.get('id',id)
    question_list = Question.objects.all()
    paginator = Paginator(question_list,1)
    page = request.GET.get('page')
    questions = paginator.get_page(page)
    return render(request,'myapp/test.html',{'user':user,'questions':questions,'page':page})

def vote(request,id,question_id,page):
    question_list = Question.objects.all()
    question = get_object_or_404(Question,pk=question_id)
    scelta = request.POST.get('choice')
    choice = Choice.objects.filter(question=question_id).filter(choice_text=scelta).values_list('punteggio',flat=True)[0]
    q = PeopleQuestions(id_test=id,question=question_id,score=choice,cat=question.cat)
    q.save()
    aux = int(page)+1
    extraversion = PeopleQuestions.objects.filter(id_test=id).filter(cat='E').aggregate(mean=Avg('score'))['mean']
    agreeableness = PeopleQuestions.objects.filter(id_test=id).filter(cat='A').aggregate(mean=Avg('score'))['mean']
    neuroticism = PeopleQuestions.objects.filter(id_test=id).filter(cat='N').aggregate(mean=Avg('score'))['mean']
    openness = PeopleQuestions.objects.filter(id_test=id).filter(cat='O').aggregate(mean=Avg('score'))['mean']
    coscientiousness = PeopleQuestions.objects.filter(id_test=id).filter(cat='C').aggregate(mean=Avg('score'))['mean']
    if(int(page) is question_list.count()):
       p= People(id_test=id,extraversion=extraversion,agreeableness=agreeableness,
                                        neuroticism=neuroticism,openness=openness,
                                        coscientiousness=coscientiousness)
       p.save()
    return render(request,'myapp/evaluation.html',{'extraversion':extraversion,
                                                   'agreeableness':agreeableness,
                                                   'neuroticism':neuroticism,
                                                   'openness':openness,
                                                   'coscientiousness':coscientiousness,
                                                   'id':id,'questions':question_list,'aux':aux})

