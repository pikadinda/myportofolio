
import uuid

from django.contrib.auth.models import Group, User
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient, APITestCase

from main.models import Experience


class ExperienceAPITest(APITestCase):

    def setUp(self):
        self.owner = User.objects.create_superuser(
            username="owner",
            password="test-password",
            email="owner@example.com",
        )

        self.visitor = User.objects.create_user(
            username="visitor",
            password="test-password",
        )

        self.experience = Experience.objects.create(
            title="Portfolio Experience",
            description="My portfolio experience",
            category="volunteer",
        )

        self.initial_experience_count = Experience.objects.count()

        self.list_url = reverse("api:experience-list")

        self.detail_url = reverse(
            "api:experience-detail",
            args=[self.experience.id],
        )

        self.star_url = reverse(
            "api:experience-star",
            args=[self.experience.id],
        )

        self.payload = {
            "title": "New Experience",
            "description": "A useful experience",
            "category": "research",
            "thumbnail": "",
        }

    def test_public_list_and_detail(self):
        response = self.client.get(self.list_url)

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        # Cari data Experience milik test ini berdasarkan UUID.
        experience_data = next(
            (
                item for item in response.data
                if str(item["id"]) == str(self.experience.id)
            ),
            None,
        )

        self.assertIsNotNone(experience_data)
        self.assertFalse(experience_data["is_starred"])
        self.assertNotIn("fields", experience_data)

        # Uji endpoint detail.
        detail_response = self.client.get(self.detail_url)

        self.assertEqual(
            detail_response.status_code,
            status.HTTP_200_OK,
        )
        self.assertEqual(
            str(detail_response.data["id"]),
            str(self.experience.id),
        )

    def test_search_and_empty_results(self):
        response = self.client.get(
            self.list_url,
            {"title": "PORT"},
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertEqual(len(response.data), 1)

        response = self.client.get(
            self.list_url,
            {"title": "not-found"},
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertEqual(response.data, [])

    def test_missing_experience(self):
        url = reverse(
            "api:experience-detail",
            args=[uuid.uuid4()],
        )

        response = self.client.get(url)

        self.assertEqual(
            response.status_code,
            status.HTTP_404_NOT_FOUND,
        )

    def test_guest_and_visitor_cannot_write(self):
        for user in (None, self.visitor):

            self.client.force_authenticate(user=user)

            response = self.client.post(
                self.list_url,
                self.payload,
                format="json",
            )

            self.assertEqual(
                response.status_code,
                status.HTTP_403_FORBIDDEN,
            )

            response = self.client.patch(
                self.detail_url,
                {"title": "Changed"},
                format="json",
            )

            self.assertEqual(
                response.status_code,
                status.HTTP_403_FORBIDDEN,
            )

            response = self.client.delete(self.detail_url)

            self.assertEqual(
                response.status_code,
                status.HTTP_403_FORBIDDEN,
            )

        self.assertEqual(
            Experience.objects.count(),
            self.initial_experience_count,
        )

        self.experience.refresh_from_db()

        self.assertEqual(
            self.experience.title,
            "Portfolio Experience",
        )

    def test_owner_can_create(self):
        self.client.force_authenticate(user=self.owner)

        response = self.client.post(
            self.list_url,
            self.payload,
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED,
        )

        self.assertTrue(
            Experience.objects.filter(
                pk=response.data["id"]
            ).exists()
        )

    def test_validation(self):
        self.client.force_authenticate(user=self.owner)

        invalid_inputs = [
            {"title": "   "},
            {
                "title": '<img src="x" onerror="alert(1)">'
            },
        ]

        for changes in invalid_inputs:

            payload = {
                **self.payload,
                **changes,
            }

            response = self.client.post(
                self.list_url,
                payload,
                format="json",
            )

            self.assertEqual(
                response.status_code,
                status.HTTP_400_BAD_REQUEST,
            )

            self.assertIn("title", response.data)

        self.assertEqual(
            Experience.objects.count(),
            self.initial_experience_count,
        )

    def test_patch_put_and_delete(self):
        self.client.force_authenticate(user=self.owner)

        response = self.client.patch(
            self.detail_url,
            {"title": "Changed"},
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.experience.refresh_from_db()

        self.assertEqual(self.experience.title, "Changed")

        self.assertEqual(
            self.experience.description,
            "My portfolio experience",
        )

        response = self.client.put(
            self.detail_url,
            {"title": "Incomplete"},
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
        )

        response = self.client.put(
            self.detail_url,
            self.payload,
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        response = self.client.delete(self.detail_url)

        self.assertEqual(
            response.status_code,
            status.HTTP_204_NO_CONTENT,
        )

        self.assertEqual(response.content, b"")

        self.assertFalse(
            Experience.objects.filter(
                pk=self.experience.id
            ).exists()
        )

    def test_star_requires_login_and_toggles(self):
        response = self.client.post(self.star_url)

        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN,
        )

        self.client.force_authenticate(user=self.visitor)

        response = self.client.post(self.star_url)

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertTrue(response.data["is_starred"])
        self.assertEqual(response.data["star_count"], 1)

        response = self.client.post(self.star_url)

        self.assertFalse(response.data["is_starred"])
        self.assertEqual(response.data["star_count"], 0)

    def test_computed_fields_are_read_only(self):
        self.client.force_authenticate(user=self.owner)

        response = self.client.post(
            self.list_url,
            {
                **self.payload,
                "star_count": 99,
                "is_starred": True,
                "starred_by_names": "forged",
                "starred_by": [self.visitor.id],
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED,
        )

        self.assertEqual(response.data["star_count"], 0)

        self.assertFalse(response.data["is_starred"])

        self.assertEqual(response.data["starred_by_names"], "")

    def test_staff_and_editor_permissions(self):

        staff = User.objects.create_user(
            username="staff",
            password="test-password",
            is_staff=True,
        )

        editor = User.objects.create_user(
            username="editor",
            password="test-password",
        )

        editor_group, _ = Group.objects.get_or_create(
            name="Editor",
        )

        editor.groups.add(editor_group)

        # Staff tanpa grup Editor tidak boleh mengubah Experience.
        self.client.force_authenticate(user=staff)

        response = self.client.patch(
            self.detail_url,
            {"title": "Staff Update"},
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN,
        )

        # Editor boleh melakukan PATCH.
        self.client.force_authenticate(user=editor)

        response = self.client.patch(
            self.detail_url,
            {"title": "Editor Update"},
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        # Editor juga boleh melakukan PUT.
        response = self.client.put(
            self.detail_url,
            self.payload,
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        # Editor tidak boleh membuat Experience.
        response = self.client.post(
            self.list_url,
            self.payload,
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN,
        )

        # Editor tidak boleh menghapus Experience.
        response = self.client.delete(self.detail_url)

        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN,
        )

    def test_wrong_method(self):
        self.client.force_authenticate(user=self.owner)

        response = self.client.delete(self.list_url)

        self.assertEqual(
            response.status_code,
            status.HTTP_405_METHOD_NOT_ALLOWED,
        )

        response = self.client.get(self.star_url)

        self.assertEqual(
            response.status_code,
            status.HTTP_405_METHOD_NOT_ALLOWED,
        )

    def test_session_write_without_csrf_is_rejected(self):
        client = APIClient(enforce_csrf_checks=True)

        self.assertTrue(
            client.login(
                username="owner",
                password="test-password",
            )
        )

        response = client.post(
            self.list_url,
            self.payload,
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN,
        )

        self.assertEqual(
            Experience.objects.count(),
            self.initial_experience_count,
        )

    def test_session_write_with_csrf_succeeds(self):
        client = APIClient(enforce_csrf_checks=True)

        self.assertTrue(
            client.login(
                username="owner",
                password="test-password",
            )
        )

        # Meminta Browsable API untuk menghasilkan CSRF token.
        page = client.get(
            self.list_url,
            HTTP_ACCEPT="text/html",
        )

        self.assertEqual(
            page.status_code,
            status.HTTP_200_OK,
        )

        token = client.cookies["csrftoken"].value

        response = client.post(
            self.list_url,
            self.payload,
            format="json",
            HTTP_X_CSRFTOKEN=token,
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED,
        )
