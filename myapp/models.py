from django.contrib.auth.models import User
from django.db import models

# Create your models here.
class Question(models.Model):
    question_text = models.CharField(max_length=200)
    cat = models.CharField(max_length=3)
    def __str__(self):
        return self.question_text

class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=100)
    punteggio = models.IntegerField(default=0)
    def __str__(self):
        return self.choice_text

class Email(models.Model):
    email_comma_separated = models.TextField(default='Enter the emails here:')
    text = models.TextField(default='Enter the text here:')
    oggetto = models.TextField(default='Enter the object here:')
    def __str__(self):
        return self.email_comma_separated

class Result(models.Model):
    id_test = models.CharField(max_length=10,primary_key=True)
    email = models.CharField(max_length=50)
    extraversion = models.FloatField(default=0.0)
    coscientiousness = models.FloatField(default=0.0)
    agreeableness = models.FloatField(default=0.0)
    openness = models.FloatField(default=0.0)
    neuroticism = models.FloatField(default=0.0)

class Question_people(models.Model):
    id_test = models.CharField(max_length=10)
    email = models.CharField(max_length=50)
    question = models.IntegerField(default=0)
    score = models.IntegerField(default=0)
    cat = models.CharField(max_length=3)

class EmailToken(models.Model):
    email = models.CharField(max_length=50)
    id_test = models.CharField(max_length=10)

class FurtherPeopleInfo(models.Model):
    id_test = models.CharField(max_length=10)
    email = models.CharField(max_length=50)
    date_of_birth = models.CharField(max_length=30)
    born = models.CharField(max_length=100)
    gender = models.CharField(max_length=10)
    ethnicity = models.CharField(max_length=100)
    level_school = models.CharField(max_length=100)
    employment = models.CharField(max_length=100)


