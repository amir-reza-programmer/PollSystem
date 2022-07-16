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


class CandidateChoiceForm(forms.Form):
    def __init__(self, choices_object, *args, **kwargs):
        """
        Initialize label & field
        :returns None:
        """
        # choices_object = kwargs.pop('choices_object')  # A Question object
        super(CandidateChoiceForm, self).__init__(*args, **kwargs)
        # if question.type == Types.RADIO:
        #     choices_ = [(op.id, op) for op in question.option_set.all()]
        #     self.fields['answer'] = forms.ChoiceField(label=question.statement,
        #                                               initial=1,
        #                                               widget=forms.RadioSelect,
        #                                               choices=choices_)
        # elif question.type == Types.CHECKBOX:
        question_statement = 'choose who can take this survey:'
        all_choices = [(choices_object[index].user_id, choices_object[index].username) for index in
                       range(len(choices_object))]
        all_choices = tuple(all_choices)
        print(all_choices)
        chosen_choices = []
        for index in range(len(choices_object)):
            if choices_object[index].is_chosen:
                chosen_choices.append(choices_object[index].user_id)
        # chosen_choices = tuple(chosen_choices)
        self.fields['ultimate_chosen'] = forms.MultipleChoiceField(label=question_statement,
                                                                   initial=chosen_choices,
                                                                   widget=forms.CheckboxSelectMultiple,
                                                                   choices=all_choices)
        # DEMO_CHOICES = (
        #     ("1", "Naveen"),
        #     ("2", "Pranav"),
        #     ("3", "Isha"),
        #     ("4", "Saloni"),
        # )
        # self.fields['ultimate_chosen'] = forms.MultipleChoiceField(choices=DEMO_CHOICES)


# choices_dict = ['ali', 'sfs', 'fsss']
# choices_ = [(index + 1, choices_dict[index].name) for index in range(len(choices_dict))]
# print(choices_)

class AnswerSheetForm(forms.Form):
    def __init__(self, question, the_choices, *args, **kwargs):
        """
        Initialize label & field
        :returns None:
        """
        # choices_object = kwargs.pop('choices_object')  # A Question object
        super(AnswerSheetForm, self).__init__(*args, **kwargs)
        # if question.type == Types.RADIO:
        #     choices_ = [(op.id, op) for op in question.option_set.all()]
        #     self.fields['answer'] = forms.ChoiceField(label=question.statement,
        #                                               initial=1,
        #                                               widget=forms.RadioSelect,
        #                                               choices=choices_)
        # elif question.type == Types.CHECKBOX:
        question_statement = question
        # all_choices = [(choices_object[index].user_id, choices_object[index].username) for index in
        #                range(len(choices_object))]
        # all_choices = tuple(all_choices)
        # print(all_choices)
        # choices = []
        # for index in range(len(choices_)):
        #     if choice_objects[index].is_chosen:
        #         choices.append({choice_objects[index].id: choice_objects[index].text})
        initial_choice = []
        if len(the_choices) > 0:
            initial_choice = the_choices[0]
        # chosen_choices = tuple(chosen_choices)
        self.fields['chosen_choice'] = forms.ChoiceField(label=question_statement,
                                                         initial=initial_choice,
                                                         widget=forms.RadioSelect,
                                                         choices=the_choices)
