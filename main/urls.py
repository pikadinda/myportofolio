from django.urls import path

from . import views

app_name = "main"

urlpatterns = [
    path("", views.show_main, name="show_main"),
    path("education/", views.show_education, name="show_education"),
    path("experience/", views.show_experience, name="show_experience"),
    path("experience/add/", views.show_experience_form, name="show_experience_form"),
    path(
        "experience/<uuid:experience_id>/edit/",
        views.edit_experience,
        name="edit_experience",
),

    path("skills/", views.show_skills, name="show_skills"),
    path("interests/", views.show_interests, name="show_interests"),
    path("skills/add/", views.show_skill_form, name="show_skill_form"),
    path("api/skills/", views.get_skills_json, name="get_skills_json"),
    path("skills/<int:skill_id>/delete/", views.delete_skill, name="delete_skill"),
]