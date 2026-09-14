

# Create your views here.
from django.shortcuts import render

from main.models import Experience, Skill, Interest


def show_main(request):
    context = {
        "name": "Adinda Pika Fauziah",
        "npm": "2506533646",
        "study_program": "S1 Information Systems",
        "bio": (
            "Information Systems student at Universitas Indonesia."
            "Just a student who enjoys documenting life through photos, discovering great bakeries, and keeping things simple."
           
        ),
    }
    return render(request, "index.html", context)


def show_experience(request):
    context = {
        "name": "Adinda Pika Fauziah",
        "experience_list": Experience.objects.all(),
    }
    return render(request, "experience.html", context)


def show_skills(request):
    context = {
        "name": "Adinda Pika Fauziah",
        "skill_list": Skill.objects.all(),
    }
    return render(request, "skills.html", context)


def show_interests(request):
    context = {
        "name": "Adinda Pika Fauziah",
        "interest_list": Interest.objects.all(),
    }
    return render(request, "interests.html", context)

def show_education(request):
    context = {
        "name": "Adinda Pika Fauziah",
    }
    return render(request, "education.html", context)
