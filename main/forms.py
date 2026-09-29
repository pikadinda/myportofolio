from django import forms

from django.core.exceptions import ValidationError
from django.utils.html import strip_tags

from .models import Experience, Skill


class SkillForm(forms.ModelForm):
    class Meta:
        model = Skill
        fields = ["name", "description", "level", "category"]

class ExperienceForm(forms.ModelForm):
    class Meta:
        model = Experience
        fields = ["title", "description", "category", "thumbnail"]

    def clean_title(self):
        title = strip_tags(self.cleaned_data["title"]).strip()

        if not title:
            raise ValidationError(
                "Judul experience tidak boleh hanya berisi tag HTML."
            )

        return title

    def clean_description(self):
        return strip_tags(
            self.cleaned_data["description"]
        ).strip()
        