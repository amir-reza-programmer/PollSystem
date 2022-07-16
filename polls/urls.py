from django.urls import path, re_path
from polls import views

app_name = 'polls'
urlpatterns = [
    # path('survey', views.survey_index, name='survey'),
    path('survey/edit/<int:id>', views.edit_survey, name='edit_survey'),
    path('survey/delete_survey/<int:id>', views.delete_survey, name='delete_survey'),
    path('survey/create/question/<int:id>', views.create_question, name='create_question'),
    path('survey/create/choice/<int:id>', views.create_choice, name='create_choice'),
    path('survey/create/survey', views.create_survey, name='create_survey'),
    path('survey/choose_takers/survey/<int:id>', views.choose_takers, name='choose_takers'),
    re_path(r'^take/survey/(?P<survey_id>[0-9]+)/(?P<last_question>[0-9]+)', views.take_survey, name='take_survey'),
    path('take/survey/<int:suervey_id>/<int:question_id>', views.take_question, name='take_question'),
    path('survey/analyze/survey/<int:survey_id>', views.see_results, name='see_results'),

]