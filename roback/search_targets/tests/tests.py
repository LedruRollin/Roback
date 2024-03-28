
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from unittest.mock import patch
from datetime import datetime

from search_targets.models import SearchTarget

from .mocks import get_date_mocker, get_datetime_mocker


class TestSearchTargets(APITestCase):

    mocked_date = datetime(2000, 1, 1, 2, 2, 2)

    @patch("datetime.date", get_date_mocker(mocked_date))
    @patch("datetime.datetime", get_datetime_mocker(mocked_date))
    def setUp(self) -> None:
        self.test_search_target = SearchTarget.objects.create(
            search_text="test_text",
        )

    def test_get_all(self):
        url = reverse("search_targets-list")
        response = self.client.get(url)

        self.assertTrue(status.is_success(response.status_code))
        self.assertEqual(response.data["total-count"], 1)
        search_target = response.data["data"][0]
        self.assertEqual(search_target["search_text"], self.test_search_target.search_text)
        retrieved_creation_date = datetime.strptime(
            f'{search_target["insertion_date"]};{search_target["insertion_time"]}', 
            "%Y-%m-%d;%H:%M:%S"
        )
        self.assertEqual(retrieved_creation_date, self.mocked_date)

    def test_get(self):
        url = reverse("search_targets-detail", args=[self.test_search_target.id])
        response = self.client.get(url)
        self.assertTrue(status.is_success(response.status_code))
        self.assertEqual(response.data["id"], self.test_search_target.id)
        self.assertEqual(response.data["search_text"], self.test_search_target.search_text)

    def test_post(self):
        url = reverse("search_targets-list")
        input_post_data = {"search_text": "posted_test_text"}
        response = self.client.post(url, input_post_data)

        self.assertTrue(status.is_success(response.status_code))
        output_post_data = response.data
        self.assertTrue(input_post_data.items() <= output_post_data.items())

    def test_edit(self):
        url = reverse("search_targets-detail", args=[self.test_search_target.id])
        new_text = "edited_text"
        input_patch_data = {"search_text": new_text}
        response = self.client.patch(url, input_patch_data)

        self.assertTrue(status.is_success(response.status_code))
        self.assertEqual(response.data["search_text"], new_text)

    def test_delete(self):
        url = reverse("search_targets-detail", args=[self.test_search_target.id])
        response = self.client.delete(url)
        self.assertTrue(status.is_success(response.status_code))
