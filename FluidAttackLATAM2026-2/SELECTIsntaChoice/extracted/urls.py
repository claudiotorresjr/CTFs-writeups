from django.urls import path
from surveys import views

urlpatterns = [
    path("", views.index, name="index"),
    path("api/surveys/", views.survey_search, name="survey_search"),
    path("health/", views.health, name="health"),
]
