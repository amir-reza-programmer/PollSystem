from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, admin_required
from polls.models import Survey, Question, Choice
from django.template.defaulttags import register
from polls.forms import SurveyForm, QuestionForm, ChoiceForm

# Create your views here.


@login_required
@admin_required
def survey_index(request):
    admin_created_surveys = Survey.objects.filter(creator=request.user)
    return render(request, 'users/admin_index.html', {'admin_created_surveys': admin_created_surveys})


@login_required
@admin_required
def create_survey(request):
    if request.method == 'POST':
        # user_form = UserForm(data=request.POST)
        survey_form = SurveyForm(data=request.POST)
        if survey_form.is_valid():

            survey = survey_form.save(commit=False)
            creator = request.user
            survey.creator = creator
            survey.save()
            # should be redirected
            response = redirect('/survey/edit/' + str(survey.id))
            return response
        else:
            print(survey_form.errors)
    else:
        # user_form = UserForm()
        survey_form = SurveyForm()
        return render(request, 'polls/create_survey.html', {'survey_form': survey_form})

@login_required
@admin_required
def edit_survey(request, id):
    the_survey = Survey.objects.get(pk=id)
    questions = Question.objects.filter(survey=the_survey)
    survey_dict = {}
    for question_index in range(len(questions)):
        choices = Choice.objects.filter(question=questions[question_index])
        choices_dict = {}
        for choice_index in range(len(choices)):
            choices_dict.update({choice_index: choices[choice_index].text})
        survey_dict.update({question_index: choices_dict})

    return render(request, 'polls/edit_survey.html', {'survey_id': id, 'survey_dict': survey_dict, 'questions': questions})


@login_required
@admin_required
def delete_survey(request, id):
    Survey.objects.filter(pk=id).delete()
    response = redirect('/')
    return response


@login_required
@admin_required
def create_question(request, id):

    if request.method == 'POST':
        # user_form = UserForm(data=request.POST)
        question_form = QuestionForm(data=request.POST)
        if question_form.is_valid():

            question = question_form.save(commit=False)
            survey = Survey.objects.get(pk=id)
            question.survey = survey
            question.save()
            # should be redirected
            response = redirect('/survey/create/choice/'+str(question.id))
            return response
        else:
            print(question_form.errors)
    else:
        # user_form = UserForm()
        question_form = QuestionForm()

    return render(request, 'polls/create_question.html',
                  {'question_form': question_form})


@login_required
@admin_required
def create_choice(request, id):
    created = False
    survey = None
    if request.method == 'POST':
        # user_form = UserForm(data=request.POST)
        choice_form = ChoiceForm(data=request.POST)
        if choice_form.is_valid():

            choice = choice_form.save(commit=False)
            question = Question.objects.get(pk=id)
            choice.question = question
            survey = question.survey
            choice.save()
            created = True
            # should be redirected

        else:
            print(choice_form.errors)
    else:
        # user_form = UserForm()
        choice_form = ChoiceForm()
    return render(request, 'polls/create_choice.html',
                  {'choice_form': choice_form, 'created': created, 'survey': survey, 'id': id})


@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)


@register.filter
def get_array_item(array, key):
    return array[key]


@register.filter
def get_text(array):
    return array.text
