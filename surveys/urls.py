from django.urls import path

from . import views

app_name = "surveys"

urlpatterns = [
    path("", views.survey_form, name="form"),
    path("thanks/", views.thank_you, name="thank_you"),
]

