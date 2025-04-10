from django.urls import path
from . import views
urlpatterns = [
    path('', views.index, name='home.index'),
    path('about', views.about, name='home.about'),
    path('dashboard', views.dashboard, name='home.dashboard'),
    path('api/button-action/', views.api_button_action, name='api_button_action')

]