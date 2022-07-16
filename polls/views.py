from django.db.models.functions import math
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, admin_required, user_required
from polls.models import SurveyUser, Survey, Question, Choice, CandidateUsers, Answer
from django.template.defaulttags import register
from polls.forms import SurveyForm, QuestionForm, ChoiceForm, CandidateChoiceForm, AnswerSheetForm


# Create your views here.


@login_required
@admin_required(login_url='/login')
def admin_survey_index(request):
    admin_created_surveys = Survey.objects.filter(creator=request.user)
    return render(request, 'users/admin_index.html', {'admin_created_surveys': admin_created_surveys})


@login_required
@user_required(login_url='/login')
def user_survey_index(request):
    user = request.user
    answers = Answer.objects.filter(user=user)
    participated_surveys = []
    for answer in answers:
        survey = answer.choice.question.survey
        participated_surveys.append(survey)
    participated_surveys = list(set(participated_surveys))
    candidate_users = CandidateUsers.objects.filter(survey_taker=user)
    all_other_surveys = []
    for candidate_user in candidate_users:
        all_other_surveys.append(candidate_user.survey)
    for participated_survey in participated_surveys:
        # all_other_surveys = all_other_surveys.exclude(survey=participated_survey)
        if participated_survey in all_other_surveys:
            all_other_surveys.remove(participated_survey)
    print(participated_surveys)
    print(all_other_surveys)
    participated_surveys_zero = len(participated_surveys) == 0
    all_other_surveys_zero = len(all_other_surveys) == 0
    return render(request, 'users/user_index.html', {'participated_surveys_zero': participated_surveys_zero, 'all_other_surveys_zero': all_other_surveys_zero, 'participated_surveys': participated_surveys, 'all_other_surveys': all_other_surveys, 'last_question_id': 0})


the_survey_question_index = -1


@login_required
@user_required(login_url='/login')
def take_survey(request, survey_id, last_question):
    print(last_question)
    user = request.user
    the_survey = Survey.objects.get(pk=survey_id)
    questions = Question.objects.filter(survey=the_survey)
    print(int(last_question) == 0)
    if int(last_question) == 0:
        return take_question(request, questions, 0)
            # render(request, 'take/survey/' + str(survey_id) + '/' + str(survey_id), {'question_element': question_element})
        # response = redirect('take/survey/' + str(survey_id) + '/' + str(survey_id))
    else:
        if int(last_question) < len(questions):
            return take_question(request, questions, last_question)
        else:
            return render(request, 'polls/finished_survey.html')


@login_required
@user_required(login_url='/login')
def take_question(request, questions, question_index):
    user = request.user
    the_question = questions[int(question_index)]
    survey_id = the_question.survey.id
    choices = Choice.objects.filter(question=the_question)
    the_choices = []
    for choice_index in range(len(choices)):
        the_choices.append((choices[choice_index].id, choices[choice_index].text))
    print(request.method)
    if request.method == 'POST':
        # user_form = UserForm(data=request.POST)
        answer_form = AnswerSheetForm(data=request.POST, question=the_question.text, the_choices=the_choices)
        if answer_form.is_valid():

            answers = answer_form.cleaned_data.get("chosen_choice")
            choice = Choice.objects.get(pk=answers)
            question = choice.question
            possible_choices = Choice.objects.filter(question=question)
            for possible_choice in possible_choices:
                Answer.objects.filter(choice=possible_choice).filter(user=request.user).delete()
            new_answer = Answer(choice=choice, user=request.user)
            new_answer.save()
            print(choice.text)

            response = redirect('/take/survey/'+str(survey_id) + '/' + str(int(question_index) + 1))
            return response
        else:
            print(answer_form.errors)
    else:
        answer_form = AnswerSheetForm(question=the_question.text, the_choices=the_choices)
        return render(request, 'polls/answer_question.html', {'answer_form': answer_form})


    # survey_dict = {}
    # for question_index in range(len(questions)):
    #     choices = Choice.objects.filter(question=questions[question_index])
    #     choices_dict = {}
    #     for choice_index in range(len(choices)):
    #         choices_dict.update({choice_index: choices[choice_index].text})
    #     survey_dict.update({question_index: choices_dict})
    # response = redirect('/survey/create/choice/' + str(survey_id))
    # return response


def see_participated_survey(request):
    pass


@login_required
@admin_required(login_url='/login')
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
@admin_required(login_url='/login')
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
@admin_required(login_url='/login')
def delete_survey(request, id):
    Survey.objects.filter(pk=id).delete()
    response = redirect('/')
    return response


@login_required
@admin_required(login_url='/login')
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
@admin_required(login_url='/login')
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
@admin_required(login_url='/login')
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


@login_required
@admin_required(login_url='/login')
def see_results(request, survey_id):
    the_survey = Survey.objects.get(pk=survey_id)
    questions = Question.objects.filter(survey=the_survey)
    survey_dict = {}
    survey_result_dict = {}
    for question_index in range(len(questions)):
        choices = Choice.objects.filter(question=questions[question_index])
        choices_dict = {}
        choices_result_dict = {}
        the_sum = 0
        for choice_index in range(len(choices)):
            choice_number = len(Answer.objects.filter(choice=choices[choice_index]))
            print('choice number', choice_number)
            choices_result_dict.update({choice_index: choice_number})
            the_sum += choice_number
        print('the sum' ,the_sum)
        for choice_index in range(len(choices)):
            choice_percent = str(round((choices_result_dict.get(choice_index)/the_sum) * 100))
            choices_dict.update({choice_index: choices[choice_index].text})
            choices_result_dict.update({choice_index: choice_percent})
        survey_dict.update({question_index: choices_dict})
        survey_result_dict.update({question_index: choices_result_dict})

    return render(request, 'polls/see_results.html',
                  {'survey_id': survey_id, 'survey_dict': survey_dict, 'questions': questions, 'survey_result_dict': survey_result_dict})


@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)


@register.filter
def get_array_item(array, key):
    return array[key]


@register.filter
def get_text(array):
    return array.text
