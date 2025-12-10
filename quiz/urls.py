from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('signup/', views.signup_view, name='signup'),
    path('login/', auth_views.LoginView.as_view(template_name='quiz/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

    path('dashboard/', views.dashboard, name='dashboard'),
    path('start/<int:category_id>/', views.start_quiz, name='start_quiz'),
    path('quiz/<int:category_id>/', views.quiz_view, name='quiz_view'),

    path('result/<int:result_id>/', views.result_view, name='result_view'),
]

