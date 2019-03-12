import os, json, datetime
from django.contrib import admin, messages
from django.http import HttpResponseRedirect
from .models import Question, Choice, Email, Result, Question_people, EmailToken, FurtherPeopleInfo
from django.contrib.auth.models import Group, User
from myproject.logger import logger_file
from miniipip.admin_sending_mail import ModelEmail, running


# actions to save the results into file .json
def writeToJSONFile(fileName, data):
    now = datetime.datetime.now()
    filePathNameWExt = fileName
    try:
        with open(os.path.join("miniipip", "results", "{0}{1}.json".format(filePathNameWExt, now.strftime('%m-%d-%y'))),
                  "w") as fp:
            json.dump(data, fp, indent=4)
            return 1
    except Exception as e:
        logger_file(e)


def save_as_json_results(modeladmin, request, queryset):
    results = list(Result.objects.values())
    if writeToJSONFile('results', results) is 1:
        messages.success(request, "Saved correctly!")


def save_as_json_people_quest(modeladmin, request, queryset):
    results = list(Question_people.objects.values())
    if writeToJSONFile('people_questions', results) is 1:
        messages.success(request, "Saved correctly!")


class PeopleAvg(admin.ModelAdmin):
    actions = [save_as_json_results, ]
    list_display = (
        'id_test', 'time', 'email', 'openness', 'coscientiousness', 'extraversion', 'agreeableness', 'neuroticism')


class EmailTokenOne(admin.ModelAdmin):
    list_display = ('id_test', 'email')


admin.site.register(Result, PeopleAvg)


class PeopleQ(admin.ModelAdmin):
    actions = [save_as_json_people_quest, ]
    list_display = ('id_test', 'email', 'question', 'score', 'cat')


admin.site.register(Question_people, PeopleQ)


class ChoiceinLine(admin.TabularInline):
    model = Choice
    extra = 0


class QuestionAdmin(admin.ModelAdmin):
    list_display = ('question_text', 'cat')
    fieldsets = [
        (None, {'fields': ['question_text']}),
        ('Categoria', {'fields': ['cat']})
    ]
    inlines = [ChoiceinLine]


admin.site.register(Question, QuestionAdmin)


class Send_email(admin.ModelAdmin):
    list_display = ('block',)
    change_form_template = "admin/change_.html"

    def response_change(self, request, obj):
        if "send-mail" in request.POST:
            # take the emails from text area and send to people with different tokens
            email_to_send = request.POST.get('email_line_by_line').splitlines()
            checked_mail = check_send_email(email_to_send)
            if len(checked_mail) is not 0:
                subject = request.POST.get('subject')
                text_sending = request.POST.get('text')
                ModelEmail.subject = subject
                ModelEmail.text = text_sending
                ModelEmail.email = checked_mail
                running()
                clean_file_json()
            return HttpResponseRedirect(".")
        self.change = super().response_change(request, obj)
        return self.change


def clean_file_json():
    with open('myproject/ajax_files/status.json', 'w') as f:
        data = {"number_of_emails_sent": 0,
                "number_of_total_emails": 0,
                "number_of_not_sent_emails": 0}
        json.dump(data, f)
        f.close()


def check_send_email(email_to_send):
    mailing_list = []
    for email in email_to_send:
        # check that the email hasn't already been sent and there are not duplicates
        if email not in EmailToken.objects.values_list('email', flat=True):
            mailing_list.append(email)
    return mailing_list


admin.site.register(Email, Send_email)
admin.site.register(EmailToken, EmailTokenOne)


class FurtherInformation(admin.ModelAdmin):
    list_display = ('id_test', 'email', 'date_of_birth', 'born', 'gender', 'ethnicity', 'level_school', 'employment')


admin.site.register(FurtherPeopleInfo, FurtherInformation)

# remove Group and User from Admin page
admin.site.unregister(User)
admin.site.unregister(Group)
