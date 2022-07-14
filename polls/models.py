from django.db import models
from users.models import SurveyUser


# Create your models here.
class Survey(models.Model):
    title = models.CharField(max_length=25, default='untitled')
    creator = models.ForeignKey(SurveyUser, on_delete=models.CASCADE)


class Question(models.Model):
    text = models.CharField(max_length=350)
    survey = models.ForeignKey(Survey, on_delete=models.CASCADE)


class Choice(models.Model):
    text = models.CharField(max_length=150)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)


class CandidateUsers(models.Model):
    survey_creator = models.ForeignKey(SurveyUser, related_name='survey_creator', on_delete=models.CASCADE)
    survey_taker = models.ForeignKey(SurveyUser, related_query_name='survey_taker', on_delete=models.CASCADE)


class Answer(models.Model):
    user = models.ForeignKey(SurveyUser, on_delete=models.CASCADE)
    choice = models.ForeignKey(Choice, on_delete=models.CASCADE)


