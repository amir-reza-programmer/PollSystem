from django.urls import path

from . import views

app_name = 'users'
urlpatterns = [
    path('', views.index_page, name='index'),
    path('register', views.register, name='register'),
    path('register/as_user', views.user_register, name='user_register'),
    path('register/as_admin', views.admin_register, name='admin_register'),
    path('login', views.login_view, name='login'),
    path('login/as_user', views.user_login, name='user_login'),
    path('login/as_admin', views.admin_login, name='admin_login'),
    path('logout', views.logout_view, name='logout'),
    # path('<int:question_id>/', views.detail, name='detail'),
    # path('<int:question_id>/results/', views.results, name='results'),
    # path('<int:question_id>/vote/', views.vote, name='vote'),
    # path('resultsdata/<str:obj>/', views.resultsData, name='resultsdata'),
]