

# Create your views here.
from django.core import serializers
from django.http import HttpResponse

from django.shortcuts import render, redirect

from main.models import Experience, Skill, Interest

from .forms import SkillForm

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
    json_response = get_skills_json(request)
    skills = serializers.deserialize(
        "json",
        json_response.content.decode("utf-8"),
    )
    skills = [skill.object for skill in skills]

    name_query = request.GET.get("name", "").strip()

    context = {
        "name": "Adinda Pika Fauziah",
        "skill_list": skills,
        "name_query": name_query,
    }

    return render(request, "skills.html", context)

def get_skills_json(request):
    name_query = request.GET.get("name", "").strip()
    skills = Skill.objects.all()

    if name_query:
        skills = skills.filter(name__icontains=name_query)

    skills_json = serializers.serialize("json", skills)
    return HttpResponse(skills_json, content_type="application/json")

def delete_skill(request, skill_id):
    if request.method == "POST":
        skill = Skill.objects.get(id=skill_id)
        skill.delete()

    return redirect("main:show_skills")

def show_skill_form(request):
    form = SkillForm()

    if request.method == "POST":
        form = SkillForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect("main:show_skills")

    context = {
        "name": "Adinda Pika Fauziah",
        "form": form,
    }

    return render(request, "skill_form.html", context)



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


