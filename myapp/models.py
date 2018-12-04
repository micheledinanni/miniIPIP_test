from django.db import models

# Create your models here.
class Question(models.Model):
    question_text = models.CharField(max_length=200)
    cat = models.CharField(max_length=3)
    score = models.IntegerField(default=0)
    def __str__(self):
        return self.question_text

class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=100)
    punteggio = models.IntegerField(default=0)
    def __str__(self):
        return self.choice_text

class People(models.Model):
    id_test = models.IntegerField(default=0)
    extraversion = models.FloatField(default=0)
    coscientiousness = models.FloatField(default=0)
    agreeableness = models.FloatField(default=0)
    openness = models.FloatField(default=0)
    neuroticism = models.FloatField(default=0)


