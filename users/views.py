from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse  # watch it's different

from users.forms import UserForm, SurveyUserForm
from django.contrib.auth import logout, authenticate, login
from django.http import HttpResponse, HttpResponseRedirect

from polls.views import survey_index


# Create your views here.
def index_page(request):
    context = {}
    print(request)
    print(request.user.is_authenticated)
    print(request.user)

    if request.user.is_authenticated:
        print(type(request.user.profile_pic))
        if request.user.is_admin:
            return survey_index(request)
        else:
            return render(request, 'users/user_index.html', context)

    else:
        return render(request, 'users/index.html', context)


def register(request):
    if request.user.is_authenticated:
        response = redirect('/')
        return response
    context = {}
    return render(request, 'users/register.html', context)


def admin_register(request):
    if request.user.is_authenticated:
        response = redirect('/')
        return response
    registered = False

    if request.method == 'POST':
        # user_form = UserForm(data=request.POST)
        survey_user_form = SurveyUserForm(data=request.POST)
        if survey_user_form.is_valid():
            # user = user_form.save()

            # user.save()
            survey_user = survey_user_form.save(commit=False)
            survey_user.set_password(survey_user.password)
            survey_user.is_active = False
            # survey_user.user = user
            # survey_user.user_id = user.id
            survey_user.is_admin = True
            survey_user.save()
            registered = True
        else:
            print(survey_user_form.errors)
    else:
        # user_form = UserForm()
        survey_user_form = SurveyUserForm()
    return render(request, 'users/admin_register.html',
                  {'survey_user_form': survey_user_form, 'registered': registered})


def user_register(request):
    if request.user.is_authenticated:
        response = redirect('/')
        return response
    registered = False

    if request.method == 'POST':
        # user_form = UserForm(data=request.POST)
        survey_user_form = SurveyUserForm(data=request.POST)
        if survey_user_form.is_valid():
            # user = user_form.save()

            # user.save()
            survey_user = survey_user_form.save(commit=False)
            survey_user.set_password(survey_user.password)
            survey_user.is_active = True
            # survey_user.user = user
            # survey_user.user_id = user.id
            survey_user.is_user = True
            survey_user.save()
            registered = True
        else:
            print(survey_user_form.errors)
    else:
        # user_form = UserForm()
        survey_user_form = SurveyUserForm()
    return render(request, 'users/user_register.html',
                  {'survey_user_form': survey_user_form, 'registered': registered})


def login_view(request):
    if request.user.is_authenticated:
        response = redirect('/')
        return response
    context = {}
    return render(request, 'users/login.html', context)


def user_login(request):
    if request.user.is_authenticated:
        response = redirect('/')
        return response
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        print(username)
        print(password)
        user = authenticate(username=username, password=password)
        content1 = '<body style="text-align: center; font: sans-serif;"><h2 style="margin-top: 30px;">you can not log in as student!</h2></body>'
        content2 = '<body style="font: sans-serif;"><h2 style="text-align: center; margin-top: 30px;">entered creditionals were wrong.</h2></body>'


        print(user)
        if user:
            if user.is_user:
                login(request, user)

                response = redirect('/')
                return response
            else:
                return HttpResponse(content2)
        else:
            return HttpResponse(content1)
    else:
        return render(request, 'users/user_login.html', {})


def admin_login(request):
    if request.user.is_authenticated:
        response = redirect('/')
        return response
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        print(username)
        print(password)
        user = authenticate(username=username, password=password)
        content1 = '<body style="text-align: center; font: sans-serif;"><h2 style="margin-top: 30px;">you can not log in as admin!</h2></body>'
        content2 = '<body style="font: sans-serif;"><h2 style="text-align: center; margin-top: 30px;">ERROR</h2><P>the reason may be: <br> 1) entered creditionals were wrong. <br> 2) your account is not activated yet!</P></body>'
        print(user)
        if user:
            if user.is_admin:

                login(request, user)

                response = redirect('/')
                return response
            else:
                return HttpResponse(content1)
        else:
            return HttpResponse(content2)
    else:
        return render(request, 'users/admin_login.html', {})


@login_required
def logout_view(request):
    logout(request)
    response = redirect('/')
    return response
