from tkinter import filedialog
from django.contrib import admin
from django.http import HttpResponseRedirect
from django.utils.crypto import get_random_string
from .models import Question,Choice,Email,Result,Question_people,EmailToken,FurtherPeopleInfo
from django.core.mail import send_mail
from django.contrib.auth.models import Group,User
import tkinter,json,re
from django.conf import settings

#actions to save the results into file .json
def writeToJSONFile(path,fileName,data):
    filePathNameWExt = '' + path + '/' + fileName + '.json'
    with open(filePathNameWExt,'w') as fp:
        json.dump(data,fp)

def save_as_json_results(modeladmin, request, queryset):
    top = tkinter.Tk()
    in_path = filedialog.askdirectory()
    top.destroy()
    top.mainloop()
    results = list(Result.objects.values())
    writeToJSONFile(in_path,'Results',results)

def save_as_json_people_quest(modeladmin, request, queryset):
    top = tkinter.Tk()
    in_path = filedialog.askdirectory()
    top.destroy()
    top.mainloop()
    results = list(Question_people.objects.values())
    writeToJSONFile(in_path, 'PeopleQuestions', results)

class PeopleAvg(admin.ModelAdmin):
    actions = [save_as_json_results,]
    list_display = ('id_test','email','openness','coscientiousness','extraversion','agreeableness','neuroticism')

class EmailTokenOne(admin.ModelAdmin):
    list_display = ('id_test','email')

admin.site.register(Result,PeopleAvg)

class PeopleQ(admin.ModelAdmin):
    actions = [save_as_json_people_quest,]
    list_display = ('id_test','email','question','score','cat')

admin.site.register(Question_people,PeopleQ)

class ChoiceinLine(admin.TabularInline):
    model = Choice
    extra = 0

class QuestionAdmin(admin.ModelAdmin):
    list_display = ('question_text','cat')
    fieldsets = [
            (None,{'fields': ['question_text']}),
            ('Categoria', {'fields': ['cat']})
                ]
    inlines = [ChoiceinLine]
admin.site.register(Question, QuestionAdmin)

class Field_mail(admin.TabularInline):
    model = Email

class Send_email(admin.ModelAdmin):
    change_form_template = "admin/change_.html"
    def response_change(self, request, obj):
        if "send-mail" in request.POST:
            #take the emails from text area and send to people with different tokens
            email_to_send = request.POST.get('email_comma_separated').split(',')
            check_send_email(email_to_send,request)
            self.message_user(request,"Email checked and sent succesfully!")
            return HttpResponseRedirect(".")
        return super().response_change(request, obj)

def check_send_email(email_to_send,request):
    for email in email_to_send:
        # verify that the emails are correct syntactically
        if re.match(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)", email):
            # check that the email hasn't already been sent and there are not duplicates
            if email not in EmailToken.objects.values_list('email', flat=True):
                id = get_random_string(length=6)
                oggetto = request.POST.get('oggetto')
                text_to_send = request.POST.get('text')
                send_mail(oggetto,
                          text_to_send + id,
                          settings.EMAIL_HOST_USER,
                          recipient_list=[email],
                          fail_silently=False)
                flag = True
                # save the token and the email in EmailToken table
                q = EmailToken(id_test=id, email=email)
                q.save()

admin.site.register(Email,Send_email)
admin.site.register(EmailToken,EmailTokenOne)

class FurtherInformation(admin.ModelAdmin):
    list_display = ('id_test','email','date_of_birth','born','gender','ethnicity','level_school','employment')
admin.site.register(FurtherPeopleInfo,FurtherInformation)

#remove Group and User from Admin page
admin.site.unregister(User)
admin.site.unregister(Group)