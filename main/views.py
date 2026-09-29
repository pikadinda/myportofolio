

# Create your views here.
import datetime
from django.core import serializers
from django.http import HttpResponse, JsonResponse

from django.shortcuts import render, redirect, get_object_or_404

from main.models import Experience, Skill, Interest

from .forms import ExperienceForm, SkillForm

from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied

from django.views.decorators.http import require_POST


def register(request):
    form = UserCreationForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Akun berhasil dibuat. Silakan login.")
        return redirect("main:login")

    context = {
        "name": "Adinda Pika Fauziah",
        "form": form,
    }

    return render(request, "register.html", context)

def login_user(request):
    form = AuthenticationForm(request, data=request.POST or None)
    if request.method == "POST" and form.is_valid():
        user = form.get_user()
        login(request, user)

        response = redirect("main:show_main")
        response.set_cookie(
            "last_login",
            datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        )

        return response

    context = {
        "name": "Adinda Pika Fauziah",
        "form": form,
    }

    return render(request, "login.html", context)

def logout_user(request):
    logout(request)

    response = redirect("main:show_main")
    response.delete_cookie("last_login")
    return response

def show_main(request):
    last_login = request.COOKIES.get(
    "last_login",
    "Belum ada sesi login / Cookie tidak ditemukan"
    )

    context = {
        "name": "Adinda Pika Fauziah",
        "npm": "2506533646",
        "study_program": "S1 Information Systems",
        "bio": (
            "Information Systems student at Universitas Indonesia."
            "Just a student who enjoys documenting life through photos, discovering great bakeries, and keeping things simple."
           
        ),
        "last_login": last_login,
    }
    return render(request, "index.html", context)


def show_experience(request):

    is_editor = request.user.groups.filter(name="Editor").exists()

    context = {
        "name": "Adinda Pika Fauziah",
        "is_editor": is_editor,
        "form": ExperienceForm(),
    }
    return render(request, "experience.html", context)

def get_experiences_json(request):
    search_query = request.GET.get("title", "").strip()

    experiences = Experience.objects.prefetch_related("starred_by").all()

    if search_query:
        experiences = experiences.filter(title__icontains=search_query)

    data = []

    for experience in experiences:
        starred_users = experience.starred_by.all()

        is_starred = (
            request.user in starred_users
            if request.user.is_authenticated
            else False
        )

        starred_by_names = ", ".join(
            [user.username for user in starred_users]
        )
        data.append({
            "pk": str(experience.id),
            "fields": {
                "title": experience.title,
                "description": experience.description,
                "category": experience.get_category_display(),
                "is_ongoing": experience.is_ongoing,
                "star_count": starred_users.count(),
                "is_starred": is_starred,
                "starred_by_names": starred_by_names,
            },
        })

    return JsonResponse(data, safe=False)

@login_required(login_url="/login/")
def show_experience_form(request):
    if not request.user.is_superuser:
        raise PermissionDenied
     
    form = ExperienceForm()

    if request.method == "POST":
        form = ExperienceForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect("main:show_experience")

    context = {
        "form": form,
    }

    return render(request, "experience_form.html", context)

@login_required(login_url="/login/")
def edit_experience(request, experience_id):
    is_editor = request.user.groups.filter(name="Editor").exists()
    if not request.user.is_superuser and not is_editor:
        raise PermissionDenied

    experience = get_object_or_404(Experience, id=experience_id)

    if request.method == "POST":
        form = ExperienceForm(request.POST, instance=experience)

        if form.is_valid():
            form.save()
            return redirect("main:show_experience")
    else:
        form = ExperienceForm(instance=experience)

    context = {
        "form": form,
        "experience": experience,
    }

    return render(request, "experience_form.html", context)

@login_required(login_url="/login/")
def delete_experience(request, experience_id):
    if not request.user.is_superuser:
        raise PermissionDenied
    
    if request.method == "POST":
        experience = get_object_or_404(Experience, id=experience_id)
        experience.delete()

    return redirect("main:show_experience")

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

@login_required(login_url="/login/")
def toggle_star(request, experience_id):
    experience = get_object_or_404(Experience, pk=experience_id)

    if request.method == "POST":
        if request.user in experience.starred_by.all():
            experience.starred_by.remove(request.user)
        else:
            experience.starred_by.add(request.user)

    return redirect("main:show_experience")


@require_POST
def create_experience_ajax(request):
    if not request.user.is_superuser:
        return JsonResponse(
            {
                "message": "Hanya pemilik portofolio yang dapat menambahkan experience."
            },
            status=403,
        )

    form = ExperienceForm(request.POST)

    if form.is_valid():
        experience = form.save()

        return JsonResponse(
            {
                "message": "Experience berhasil ditambahkan.",
                "pk": str(experience.id),
            },
            status=201,
        )

    return JsonResponse(
        {
            "errors": form.errors.get_json_data()
        },
        status=400,
    )

