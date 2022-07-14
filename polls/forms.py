from django import forms
from django.contrib.auth.models import User

from polls.models import Survey, Question, Choice


class SurveyForm(forms.ModelForm):

    class Meta:
        model = Survey
        fields = ('title',)


class QuestionForm(forms.ModelForm):

    class Meta:
        model = Question
        fields = ('text',)


class ChoiceForm(forms.ModelForm):

    class Meta:
        model = Choice
        fields = ('text',)


