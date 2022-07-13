from django.contrib.auth.models import User, AbstractUser
from django.db import models


# Create your models here.
class SurveyUser(AbstractUser):

    # REQUIRED_FIELDS = ('user',)
    # USERNAME_FIELD = 'user'
    # user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_pic = models.ImageField(upload_to='profile_pics', blank=True)
    is_admin = models.BooleanField(default=False)
    is_user = models.BooleanField(default=False)

    # @property
    # def is_anonymous(self):
    #     """
    #     Always return False. This is a way of comparing User objects to
    #     anonymous users.
    #     """
    #     return False

    def __str__(self):
        return self.username
# class SurveyUser(AbstractUser):
#     is_survey_user = models.BooleanField(default=True)
#     is_survey_admin = models.BooleanField(default=False)
