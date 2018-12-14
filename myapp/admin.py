from django.contrib import admin
from django.http import HttpResponseRedirect
from django.utils.crypto import get_random_string
from .models import Question,Choice,Email,People,PeopleQuestions
from django.core.mail import send_mail

class PeopleAvg(admin.ModelAdmin):
    list_display = ('id_test','extraversion','agreeableness','coscientiousness','openness','neuroticism')

admin.site.register(People,PeopleAvg)

class PeopleQ(admin.ModelAdmin):
    list_display = ('id_test','question','score','cat')

admin.site.register(PeopleQuestions,PeopleQ)

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
    #change_form_template = "admin/change_form.html"
    def response_change(self, request, obj):
        id = get_random_string(length=6)
        if "send-mail" in request.POST:
            email_to_send = request.POST.get('email')
            print (request.POST.get('email'))
            send_mail("Mini-ipip test",
                          "Here's the mini ipip test: http://127.0.0.1:8000/myapp?id={0}".format(id),
                          "michele.dinanni1@gmail.com",
                          recipient_list=[email_to_send, ],
                          fail_silently=False)
            self.message_user(request,"The email has been sent!")
        return HttpResponseRedirect(".")

admin.site.register(Email,Send_email)
