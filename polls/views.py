from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, admin_required
from polls.models import SurveyUser, Survey, Question, Choice, CandidateUsers
from django.template.defaulttags import register
from polls.forms import SurveyForm, QuestionForm, ChoiceForm, CandidateChoiceForm


# Create your views here.


@login_required
@admin_required
def admin_survey_index(request):
    admin_created_surveys = Survey.objects.filter(creator=request.user)
    return render(request, 'users/admin_index.html', {'admin_created_surveys': admin_created_surveys})


def user_survey_index(request):
    admin_created_surveys = Survey.objects.filter(creator=request.user)
    return render(request, 'users/user_index.html', {'admin_created_surveys': admin_created_surveys})


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

    return render(request, 'polls/edit_survey.html',
                  {'survey_id': id, 'survey_dict': survey_dict, 'questions': questions})


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
            response = redirect('/survey/create/choice/' + str(question.id))
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


@login_required
@admin_required
def choose_takers(request, id):
    survey = Survey.objects.get(pk=id)
    creator = survey.creator
    candidate_tuples = CandidateUsers.objects.filter(survey_creator=creator).filter(survey=survey)
    candidate_users = []
    for candidate_tuple in candidate_tuples:
        candidate_users.append(candidate_tuple.survey_taker)
    candidate_users_id = []
    all_other_users = SurveyUser.objects.filter(is_user=True)
    for candidate_user in candidate_users:
        all_other_users = all_other_users.exclude(id=candidate_user.id)
        # candidate_users_id.append(candidate_user.id)
    # candidate_users_id = candidate_users.values('id')

    # all_other_users = SurveyUser.objects.filter(is_user=True).exclude(id=candidate_users_id)
    context_users = []
    for candidate_user in candidate_users:
        taker = Taker(candidate_user.id, candidate_user.username, True)
        context_users.append(taker)
    for other_user in all_other_users:
        taker = Taker(other_user.id, other_user.username, False)
        context_users.append(taker)
    print(survey)
    print(creator)
    print(candidate_tuples)
    print(candidate_users)
    print(all_other_users)
    print(context_users)

    if request.method == 'POST':
        # user_form = UserForm(data=request.POST)
        survey_taker_form = CandidateChoiceForm(data=request.POST, choices_object=context_users)
        if survey_taker_form.is_valid():

            chosen_users = survey_taker_form.cleaned_data.get("ultimate_chosen")
            print('choosed')
            print(chosen_users)
            # should be redirected
            CandidateUsers.objects.filter(survey=survey).delete()
            for chosen_user_id in chosen_users:
                chosen_user = SurveyUser.objects.get(pk=int(chosen_user_id))
                new_candidate_user = CandidateUsers(survey_creator=creator, survey_taker=chosen_user, survey=survey)
                new_candidate_user.save()
            response = redirect('/survey/edit/' + str(id))
            return response
        else:
            print(survey_taker_form.errors)
    else:
        survey_taker_form = CandidateChoiceForm(choices_object=context_users)
        return render(request, 'polls/choose_survey_taker.html', {'survey_taker_form': survey_taker_form})


class Taker:
    def __init__(self, user_id, username, is_chosen):
        self.user_id = user_id
        self.username = username
        self.is_chosen = is_chosen


@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)


@register.filter
def get_array_item(array, key):
    return array[key]


@register.filter
def get_text(array):
    return array.text
