from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction
from django.contrib.auth.models import User

from users.models import SurveyUser


class UserForm(forms.ModelForm):
    # interests = forms.ModelMultipleChoiceField(
    #     queryset=User.objects.all(),
    #     widget=forms.CheckboxSelectMultiple,
    #     required=True
    # )

    class Meta:
        model = User
        fields = ('username', 'password')


class SurveyUserForm(forms.ModelForm):
    # interests = forms.ModelMultipleChoiceField(
    #     queryset=User.objects.all(),
    #     widget=forms.CheckboxSelectMultiple,
    #     required=True
    # )

    class Meta:
        model = SurveyUser
        fields = ('username', 'password', 'profile_pic',)

