from django.urls import path

from . import views

app_name = "main"

urlpatterns = [
    path("", views.show_main, name="show_main"),
    path("education/", views.show_education, name="show_education"),
    path("experience/", views.show_experience, name="show_experience"),
    path("skills/", views.show_skills, name="show_skills"),
    path("interests/", views.show_interests, name="show_interests"),
]