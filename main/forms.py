from django import forms
from .models import Experience, Skill


class SkillForm(forms.ModelForm):
    class Meta:
        model = Skill
        fields = ["name", "description", "level", "category"]

class ExperienceForm(forms.ModelForm):
    class Meta:
        model = Experience
        fields = ["title", "description", "category", "thumbnail"]
        