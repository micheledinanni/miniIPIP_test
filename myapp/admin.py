from tkinter import filedialog
from django.contrib import admin
from django.http import HttpResponseRedirect
from django.utils.crypto import get_random_string
from .models import Question,Choice,Email,Result,Question_people,EmailToken,FurtherPeopleInfo
from django.core.mail import send_mail
from django.contrib.auth.models import Group,User
import tkinter,json

#action to save the results into file .json
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
            #take the emails from text area and send to people with different token
            email_to_send = request.POST.get('email_comma_separated').split(',')
            for email in email_to_send:
                id = get_random_string(length=6)
                oggetto = request.POST.get('oggetto')
                text_to_send = request.POST.get('text')
                send_mail(oggetto,
                      text_to_send + id,
                      "michele.dinanni1@gmail.com",
                      recipient_list=[email],
                      fail_silently=False)
                #save the token and the email in EmailToken table
                q = EmailToken(id_test=id,email=email)
                q.save()
            self.message_user(request, "The emails have been sent!")
            return HttpResponseRedirect(".")
        return super().response_change(request, obj)

admin.site.register(Email,Send_email)
admin.site.register(EmailToken,EmailTokenOne)

class FurtherInformation(admin.ModelAdmin):
    list_display = ('id_test','email','date_of_birth','born','gender','ethnicity','level_school','employment')
admin.site.register(FurtherPeopleInfo,FurtherInformation)

#remove Group and User from Admin page
admin.site.unregister(User)
admin.site.unregister(Group)