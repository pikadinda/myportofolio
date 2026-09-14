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
        response = self.client.get(reverse("main:show_experience"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "experience.html")
        self.assertContains(response, self.experience.title)
        self.assertContains(response, self.experience.description)
        self.assertContains(response, "Part-Time")
        self.assertContains(response, "Sedang berlangsung")
        self.assertContains(response, f'href="{reverse("main:show_main")}"')

    def test_empty_experience_page(self):
        Experience.objects.all().delete()
        response = self.client.get(reverse("main:show_experience"))

        self.assertContains(response, "Belum ada pengalaman yang ditambahkan.")

    def test_completed_experience(self):
        response = self.client.get(reverse("main:show_experience"))

        self.assertContains(response, "BEM Fasilkom UI")
        self.assertContains(response, "Sedang berlangsung")

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