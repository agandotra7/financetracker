from django.urls import path
from . import views

#OPEN AI

urlpatterns = [
    path('signup', views.signup, name='accounts.signup'),
    path('login/', views.login, name='accounts.login'),
    path('logout/', views.logout, name='accounts.logout'),
    path('password_reset/', views.custom_password_reset, name='password_reset'),
    path('password_reset_done/', views.password_reset_done, name='password_reset_done'),
    path('api/advice/', views.get_financial_advice, name='get_financial_advice'),
]