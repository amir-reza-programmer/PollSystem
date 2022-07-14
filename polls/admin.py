from django.contrib import admin
from polls.models import Survey, Question, Choice, CandidateUsers, Answer
# Register your models here.
admin.site.register(Survey)
admin.site.register(Question)
admin.site.register(Choice)
admin.site.register(CandidateUsers)
admin.site.register(Answer)
