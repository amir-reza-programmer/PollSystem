from django.urls import path
from polls import views

app_name = 'polls'
urlpatterns = [
    # path('survey', views.survey_index, name='survey'),
    path('survey/edit/<int:id>', views.edit_survey, name='edit_survey'),
    path('survey/delete_survey/<int:id>', views.delete_survey, name='delete_survey'),
    path('survey/create/question/<int:id>', views.create_question, name='create_question'),
    path('survey/create/choice/<int:id>', views.create_choice, name='create_choice'),
    path('survey/create/survey', views.create_survey, name='create_survey'),
    # path('survey/create/choice/<str:id>', views.create_choice, name='create_choice'),

]