from django.utils.html import strip_tags
from rest_framework import serializers

from .models import Experience


class ExperienceSerializer(serializers.ModelSerializer):
    category_display = serializers.SerializerMethodField()
    is_ongoing = serializers.BooleanField(read_only=True)

    star_count = serializers.SerializerMethodField()
    is_starred = serializers.SerializerMethodField()
    starred_by_names = serializers.SerializerMethodField()

    class Meta:
        model = Experience
        fields = [
            "id",
            "title",
            "description",
            "category",
            "category_display",
            "thumbnail",
            "started_at",
            "ended_at",
            "is_ongoing",
            "star_count",
            "is_starred",
            "starred_by_names",
        ]
        read_only_fields = ["id", "started_at"]

    def validate_title(self, value):
        value = strip_tags(value).strip()
        if not value:
            raise serializers.ValidationError(
                "Judul experience tidak boleh hanya berisi tag HTML."
            )
        return value

    def validate_description(self, value):
        return strip_tags(value).strip()

    def get_category_display(self, obj):
        return obj.get_category_display()

    def get_star_count(self, obj):
        return obj.starred_by.count()

    def get_is_starred(self, obj):
        request = self.context.get("request")

        if request is None or not request.user.is_authenticated:
            return False

        return obj.starred_by.filter(
            pk=request.user.pk
        ).exists()

    def get_starred_by_names(self, obj):
        return ", ".join(
            obj.starred_by.values_list("username", flat=True)
        )