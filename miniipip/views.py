from django.contrib import messages
from django.utils.crypto import get_random_string
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from miniipip.sending_client_mails import ModelEmail, client_send_mail
from myproject.logger import logger_file
from .models import Question, Choice, Result, Question_people, EmailToken, FurtherPeopleInfo
from django.db.models import Avg
from miniipip.chronometer import Chronometer


def index(request, id):
    user = request.GET.get('id', '')
    if user not in EmailToken.objects.filter(id_test=user).values_list('id_test', flat=True):
        if user is '':
            identifier = EmailToken()
            user = get_random_string(length=6)
            identifier.email = 'Anonymous User'
            identifier.id_test = user
            identifier.save()
        else:
            q = EmailToken(id_test=user)
            q.save()
    return render(request, 'miniipip/index.html', {'user': user})


# create a chronometer to take test time
Chronometer_1 = Chronometer()


def test(request, id):
    try:
        user = request.GET.get('id', id)
        question_list = Question.objects.all()
        paginator = Paginator(question_list, 1)
        page = request.GET.get('page')
        if int(page) is 1:
            Chronometer_1.start()
        questions = paginator.get_page(page)
        if int(page) is Question.objects.count() + 1:
            return help_improve(request, id=id)
        else:
            return render(request, 'miniipip/test.html', {'user': user, 'questions': questions, 'page': page})
    except Exception as e:
        error = str(e)
        logger_file(error)


def vote(request, id, question_id, page):
    try:
        pagina = int(page) + 1
        email = EmailToken.objects.filter(id_test=id).values_list('email', flat=True)[0]
        question = get_object_or_404(Question, pk=question_id)
        scelta = request.POST.get('choice')
        choice = \
        Choice.objects.filter(question=question_id).filter(choice_text=scelta).values_list('punteggio', flat=True)[
            0]
        q = Question_people(id_test=id, email=email, question=question_id, score=choice, cat=question.cat)

        # if the score is already in the table, it will be replaced by new score
        if Question_people.objects.filter(id_test=id).filter(question=question_id):
            Question_people.objects.filter(id_test=id).filter(question=question_id).update(question=question_id,
                                                                                           score=choice)
        else:
            q.save()
        return HttpResponseRedirect('/miniipip/test?id={0}'.format(id) + '&page={0}'.format(pagina))
    except Exception as e:
        error = str(e)
        logger_file(error)


def results(request, id):
    Chronometer_1.stop()
    user = request.GET.get('id', id)
    time_elapsed = Chronometer_1.get_elapsed_time()
    email = EmailToken.objects.filter(id_test=user).values_list('email', flat=True)[0]
    openness = Question_people.objects.filter(id_test=user).filter(cat='O').aggregate(mean=Avg('score'))['mean']
    coscientiousness = Question_people.objects.filter(id_test=user).filter(cat='C').aggregate(mean=Avg('score'))['mean']
    extraversion = Question_people.objects.filter(id_test=user).filter(cat='E').aggregate(mean=Avg('score'))['mean']
    agreeableness = Question_people.objects.filter(id_test=user).filter(cat='A').aggregate(mean=Avg('score'))['mean']
    neuroticism = Question_people.objects.filter(id_test=user).filter(cat='N').aggregate(mean=Avg('score'))['mean']
    if user in Result.objects.filter(id_test=user).values_list('id_test', flat=True):
        Result.objects.filter(id_test=id).update(id_test=user, time=time_elapsed, email=email,
                                                 extraversion=extraversion,
                                                 agreeableness=agreeableness, openness=openness,
                                                 coscientiousness=coscientiousness, neuroticism=neuroticism)
    else:
        q = Result(id_test=user, time=time_elapsed, email=email, extraversion=extraversion, agreeableness=agreeableness,
                   openness=openness, coscientiousness=coscientiousness, neuroticism=neuroticism)
        q.save()
    if email == 'Anonymous User':
        email = ''
    return render(request, 'miniipip/evaluation.html', {'openness': openness,
                                                        'coscientiousness': coscientiousness,
                                                        'extraversion': extraversion,
                                                        'agreeableness': agreeableness,
                                                        'neuroticism': neuroticism,
                                                        'email': email})


def send_email(request, emailtosend, identifier):
    results(request, identifier)
    email_text = "I performed the mini-IPIP test and got the following scores:: \n\n" \
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
    ModelEmail.email = emailtosend
    ModelEmail.text = email_text
    if client_send_mail() is 1:
        return 1
    else:
        return 0


def help_improve(request, id):
    id = request.GET.get('id', id)
    results(request, id)
    if request.POST.get('skip'):
        return results(request, id=id)
    if request.POST.get('choice'):
        emailtosend = request.POST['email_string']
        if send_email(request, emailtosend, id) is 1:
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
                else:
                    further_info.save()
            else:
                if id not in FurtherPeopleInfo.objects.filter(id_test=id).values_list('id_test', flat=True)[0]:
                    further_info.save()
                else:
                    FurtherPeopleInfo.objects.filter(id_test=id).update(date_of_birth=further_info.date_of_birth,
                                                                        born=further_info.born,
                                                                        gender=further_info.gender,
                                                                        ethnicity=further_info.ethnicity,
                                                                        level_school=further_info.level_school,
                                                                        employment=further_info.employment)
        except Exception:
            pass
        return results(request, id=id)
    return render(request, 'miniipip/help_improve.html', {'id': id})


def redirect_root(request):
    obj = EmailToken()
    id = get_random_string(length=6)
    if id not in EmailToken.objects.filter(id_test=id).values_list('id_test', flat=True):
        obj.id_test = id
        obj.email = 'Anonymous User'
        obj.save()
    return HttpResponseRedirect('/miniipip?id={0}'.format(id))


def privacy(request):
    return render(request, 'miniipip/privacy.html')
