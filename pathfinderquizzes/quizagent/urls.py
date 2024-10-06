from django.urls import path
from . import views

urlpatterns = [
    path('', views.submit_prompt, name='submit_prompt'),
]
