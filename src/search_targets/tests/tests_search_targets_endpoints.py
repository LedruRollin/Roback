from django.contrib.auth.models import User
from django.test.client import MULTIPART_CONTENT, encode_multipart, BOUNDARY
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.test import APITestCase
from rest_framework import status
from unittest.mock import patch
from datetime import datetime

from search_targets.models import SearchTarget

from .mocks import get_date_mocker, get_datetime_mocker


class TestSearchTargetsEndpoints(APITestCase):

    endpoint = "/api/search_targets/"
    mocked_date = datetime(2000, 1, 1, 2, 2, 2)

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(username='test_user', password='test_pwd', is_staff=True)

    @patch("datetime.date", get_date_mocker(mocked_date))
    @patch("datetime.datetime", get_datetime_mocker(mocked_date))
    def setUp(self):
        self.test_search_target = SearchTarget.objects.create(
            search_text="test_text",
        )
        self.client.force_authenticate(self.user)

    def test_get_all(self):
        response = self.client.get(self.endpoint)

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
        response = self.client.get(f"{self.endpoint}{str(self.test_search_target.id)}/")

        self.assertTrue(status.is_success(response.status_code))
        self.assertEqual(response.data["id"], self.test_search_target.id)
        self.assertEqual(response.data["search_text"], self.test_search_target.search_text)

    def test_post(self):
        input_post_data = {"search_text": "posted_test_text"}
        response = self.client.post(
            self.endpoint,
            data=encode_multipart(data=input_post_data, boundary=BOUNDARY),
            content_type=MULTIPART_CONTENT,
        )

        self.assertTrue(status.is_success(response.status_code))
        output_post_data = response.data
        self.assertTrue(input_post_data.items() <= output_post_data.items())

    def test_edit(self):
        new_text = "edited_text"
        input_patch_data = {"search_text": new_text}
        response = self.client.patch(
            f"{self.endpoint}{str(self.test_search_target.id)}/",
            data=encode_multipart(data=input_patch_data, boundary=BOUNDARY),
            content_type=MULTIPART_CONTENT,
        )

        self.assertTrue(status.is_success(response.status_code))
        self.assertEqual(response.data["search_text"], new_text)

    def test_put(self):
        put_text = "put_test_text"
        input_put_data = {
            "search_text": put_text,
        }
        response = self.client.put(
            f"{self.endpoint}{str(self.test_search_target.id)}/",
            data=encode_multipart(data=input_put_data, boundary=BOUNDARY),
            content_type=MULTIPART_CONTENT,
        )

        self.assertTrue(status.is_success(response.status_code))
        self.assertEqual(response.data["search_text"], put_text)

    def test_delete(self):
        response = self.client.delete(f"{self.endpoint}{str(self.test_search_target.id)}/")
        self.assertTrue(status.is_success(response.status_code))
        with self.assertRaises(ObjectDoesNotExist):
            SearchTarget.objects.get(pk=self.test_search_target.id)
