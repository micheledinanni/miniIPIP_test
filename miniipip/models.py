from django.contrib.auth.models import User
from django.db import models


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
    df_subject = open ("default_email_subject.txt", "r").read()
    df_text = open ("default_email_text.txt", "r").read()

    block = models.AutoField(primary_key=True)
    email_line_by_line = models.TextField(default="Enter the emails here:")
    text = models.TextField(default=df_text)
    subject = models.TextField(default=df_subject)

    def __str__(self):
        return "block " + self.block.__str__()


class Result(models.Model):
    id_test = models.CharField(max_length=10, primary_key=True)
    time = models.CharField(max_length=10)
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
