from django.template import response
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from main.models import Skill

from main.models import Experience

from main.models import Interest


class MainTest(TestCase):
    def setUp(self):
        self.experience = Experience.objects.create(
            title="Asisten Dosen PBP",
            description="Membantu mahasiswa memahami pengembangan web.",
            category="part-time",
        )

    def test_main_url_is_accessible(self):
        response = self.client.get(reverse("main:show_main"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "index.html")
        self.assertNotContains(response, self.experience.title)
        self.assertContains(response, f'href="{reverse("main:show_experience")}"')

    def test_nonexistent_page_returns_404(self):
        response = self.client.get("/halaman-yang-tidak-ada/")

        self.assertEqual(response.status_code, 404)

    def test_experience_model(self):
        self.assertEqual(str(self.experience), "Asisten Dosen PBP")
        self.assertEqual(self.experience.category, "part-time")
        self.assertTrue(self.experience.is_ongoing)

    def test_experience_page(self):
        response = self.client.get(
            reverse("main:show_experience")
        )

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "experience.html")

        # Memastikan struktur halaman Experience tersedia
        self.assertContains(response, 'id="experience-search-form"')
        self.assertContains(response, 'id="search-input"')
        self.assertContains(response, 'id="loading"')
        self.assertContains(response, 'id="error"')
        self.assertContains(response, 'id="empty"')
        self.assertContains(response, 'id="grid"')

        # Memastikan halaman menggunakan API DRF
        self.assertContains(
            response,
            reverse("api:experience-list")
        )

        self.assertContains(
            response,
            f'href="{reverse("main:show_main")}"'
        )

        # Memastikan data Experience tersedia melalui API
        api_response = self.client.get(
            reverse("api:experience-list")
        )

        self.assertEqual(api_response.status_code, 200)

        experiences = api_response.json()

        experience_data = next(
            (
                item for item in experiences
                if item["id"] == str(self.experience.pk)
            ),
            None
        )

        self.assertIsNotNone(experience_data)

        self.assertEqual(
            experience_data["title"],
            self.experience.title
        )

        self.assertEqual(
            experience_data["description"],
            self.experience.description
        )

        self.assertEqual(
            experience_data["category_display"],
            "Part-Time"
        )

        self.assertTrue(
            experience_data["is_ongoing"]
        )

    def test_empty_experience_page(self):
        Experience.objects.all().delete()
        response = self.client.get(reverse("main:show_experience"))

        self.assertContains(response, "Belum ada pengalaman yang ditambahkan.")

    def test_completed_experience(self):
        completed_experience = Experience.objects.create(
            title="Pengalaman Selesai",
            description="Ini merupakan pengalaman yang sudah selesai.",
            category="volunteer",
            ended_at=timezone.now(),
        )

        response = self.client.get(
            reverse("api:experience-list")
        )

        self.assertEqual(response.status_code, 200)

        experiences = response.json()

        completed_data = next(
            (
                item for item in experiences
                if item["id"] == str(completed_experience.id)
            ),
            None
        )

        self.assertIsNotNone(completed_data)

        self.assertFalse(
            completed_data["is_ongoing"]
        )

        self.assertEqual(
            completed_data["category_display"],
            "Volunteer"
        )

class SkillPageTests(TestCase):

    def test_skill_page_uses_correct_template(self):
        response = self.client.get(reverse("main:show_skills"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "skills.html")

    def test_skill_data_appears_on_page(self):
        skill = Skill.objects.create(
            name="Test Skill",
            description="Test skill description.",
            level="Strong",
            category="Test",
        )

        response = self.client.get(reverse("main:show_skills"))

        self.assertContains(response, skill.name)
        self.assertContains(response, skill.description)
        self.assertContains(response, skill.level)

    def test_skill_page_shows_empty_state(self):
        Skill.objects.all().delete()

        response = self.client.get(reverse("main:show_skills"))

        self.assertContains(
            response,
            "No skills have been added yet."
        )

class InterestPageTests(TestCase):

    def test_interest_page_uses_correct_template(self):
        response = self.client.get(reverse("main:show_interests"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "interests.html")

    def test_interest_data_appears_on_page(self):
        interest = Interest.objects.create(
            name="Test Interest",
            description="Test interest description.",
            category="Test",
            favorite_note="Test note",
        )

        response = self.client.get(reverse("main:show_interests"))

        self.assertContains(response, interest.name)
        self.assertContains(response, interest.description)
        self.assertContains(response, interest.favorite_note)

    def test_interest_page_shows_empty_state(self):
        Interest.objects.all().delete()
        response = self.client.get(reverse("main:show_interests"))
        self.assertContains(
            response,
            "No interests have been added yet.",
    )