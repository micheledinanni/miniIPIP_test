from django.contrib import messages
from django.core.mail import send_mail
from django.utils.crypto import get_random_string
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from .models import Question, Choice, Result, Question_people, EmailToken, FurtherPeopleInfo
from django.db.models import Avg
from django.conf import settings


def index(request, id):
    user = request.GET.get('id', '')
    return render(request, 'myapp/index.html', {'user': user})


def test(request, id):
    user = request.GET.get('id', id)
    question_list = Question.objects.all()
    paginator = Paginator(question_list, 1)
    page = request.GET.get('page')
    questions = paginator.get_page(page)
    if int(page) is Question.objects.count() + 1:
        return help_improve(request, id=id)
    else:
        return render(request, 'myapp/test.html', {'user': user, 'questions': questions, 'page': page})


def vote(request, id, question_id, page):
    pagina = int(page) + 1
    email = EmailToken.objects.filter(id_test=id).values_list('email', flat=True)[0]
    question = get_object_or_404(Question, pk=question_id)
    scelta = request.POST.get('choice')
    choice = Choice.objects.filter(question=question_id).filter(choice_text=scelta).values_list('punteggio', flat=True)[
        0]
    q = Question_people(id_test=id, email=email, question=question_id, score=choice, cat=question.cat)

    # if the score is already in the table, it will be replaced by new score
    if Question_people.objects.filter(id_test=id).filter(question=question_id):
        Question_people.objects.filter(id_test=id).filter(question=question_id).update(question=question_id,
                                                                                       score=choice)
    else:
        q.save()
    return HttpResponseRedirect('/myapp/test?id={0}'.format(id) + '&page={0}'.format(pagina))


def results(request, id):
    user = request.GET.get('id', id)
    email = EmailToken.objects.filter(id_test=user).values_list('email', flat=True)[0]
    openness = Question_people.objects.filter(id_test=user).filter(cat='O').aggregate(mean=Avg('score'))['mean']
    coscientiousness = Question_people.objects.filter(id_test=user).filter(cat='C').aggregate(mean=Avg('score'))['mean']
    extraversion = Question_people.objects.filter(id_test=user).filter(cat='E').aggregate(mean=Avg('score'))['mean']
    agreeableness = Question_people.objects.filter(id_test=user).filter(cat='A').aggregate(mean=Avg('score'))['mean']
    neuroticism = Question_people.objects.filter(id_test=user).filter(cat='N').aggregate(mean=Avg('score'))['mean']
    p = Result(id_test=user, email=email, extraversion=extraversion, agreeableness=agreeableness, openness=openness,
               coscientiousness=coscientiousness, neuroticism=neuroticism)
    p.save()
    return render(request, 'myapp/evaluation.html', {'openness': openness,
                                                     'coscientiousness': coscientiousness,
                                                     'extraversion': extraversion,
                                                     'agreeableness': agreeableness,
                                                     'neuroticism': neuroticism})


def send_email(emailtosend, identifier):
    email_text = "I performed the mini-IPIP test on and i got the following scores: \n\n" \
                 "Openness: {0}".format(
        Result.objects.filter(id_test=identifier).values_list("openness", flat=True)[0]) + "/5" \
                 + "\n""Coscientiousness: {0}".format(
        Result.objects.filter(id_test=identifier).values_list("coscientiousness", flat=True)[0]) + "/5" \
                 + "\n""Extraversion: {0}".format(
        Result.objects.filter(id_test=identifier).values_list("extraversion", flat=True)[0]) + "/5" \
                 + "\n""Agreeableness: {0}".format(
        Result.objects.filter(id_test=identifier).values_list("agreeableness", flat=True)[0]) + "/5" \
                 + "\n""Neuroticism: {0}".format(
        Result.objects.filter(id_test=identifier).values_list("neuroticism", flat=True)[0]) + "/5"
    if send_mail("My results of the MiniIPIP Test",
                 email_text,
                 from_email=settings.EMAIL_HOST_USER,
                 recipient_list=[emailtosend, ], fail_silently=False) is 1:
        return 1
    return 0


def help_improve(request, id):
    id = request.GET.get('id')
    if request.POST.get('skip'):
        return results(request, id=id)
    if request.POST.get('email'):
        emailtosend = EmailToken.objects.filter(id_test=id).values_list("email", flat=True)[0]
        if send_email(emailtosend, id) is 1:
            messages.success(request, 'The email has been sent successfully!')
        return results(request, id=id)
    if request.POST.get('submit'):
        further_info = FurtherPeopleInfo()
        further_info.id_test = id
        further_info.email = EmailToken.objects.filter(id_test=id).values_list("email", flat=True)[0]
        further_info.date_of_birth = request.POST['day_of_birth']
        further_info.born = request.POST['country']
        further_info.gender = request.POST['gender']
        further_info.ethnicity = request.POST['ethnicity']
        further_info.level_school = request.POST['education']
        further_info.employment = request.POST['employment']
        try:
            if further_info.date_of_birth is '':
                if '? undefined:undefined ?' in further_info.born in further_info.gender in further_info.ethnicity \
                        in further_info.level_school in further_info.employment:
                    raise Exception
            further_info.save()
        except Exception:
            pass
        return results(request, id=id)
    return render(request, 'myapp/help_improve.html', {'id': id})


def redirect_root(request):
    return HttpResponseRedirect('/myapp?id=')
