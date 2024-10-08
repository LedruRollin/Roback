
from django.test.client import MULTIPART_CONTENT, encode_multipart, BOUNDARY
from django.core.exceptions import ObjectDoesNotExist
from django.core.files.base import ContentFile
from rest_framework.test import APITestCase
from rest_framework import status
from datetime import datetime

from search_targets.models import SearchTarget, Media


class TestMediasEndpoints(APITestCase):

    mocked_date = datetime(2000, 1, 1, 2, 2, 2)
    endpoint = "/api/medias/"

    def setUp(self) -> None:
        self.search_target = SearchTarget.objects.create(search_text="test_search_targets")
        self.media = Media.objects.create(
            search_target=self.search_target,
            name="media_name",
            file=ContentFile("test_file", name="test_file"),
            type="IMAGE"
        )

    def test_get_all(self):
        response = self.client.get(self.endpoint)

        self.assertTrue(status.is_success(response.status_code))
        self.assertEqual(response.data["total-count"], 1)
        media = response.data["data"][0]
        self.assertEqual(media["name"], self.media.name)

    def test_get(self):
        response = self.client.get(f"{self.endpoint}{str(self.media.id)}/")

        self.assertTrue(status.is_success(response.status_code))
        self.assertEqual(response.data["id"], self.media.id)
        self.assertEqual(response.data["name"], self.media.name)

    def test_post(self):
        input_post_data = {
          "name": "media_name2",
          "file": ContentFile("test_file2", name="test_file2"),
          "type": "VIDEO",
          "search_target": self.search_target.id
        }
        response = self.client.post(
            self.endpoint,
            data=encode_multipart(data=input_post_data, boundary=BOUNDARY),
            content_type=MULTIPART_CONTENT,
        )

        self.assertTrue(status.is_success(response.status_code))
        output_post_data = response.data
        self.assertEqual(input_post_data["name"], output_post_data["name"])
        self.assertEqual(input_post_data["type"], output_post_data["type"])

    def test_patch(self):
        new_name = "a_whole_new_name"
        input_patch_data = {"name": new_name}
        response = self.client.patch(
            f"{self.endpoint}{str(self.media.id)}/",
            data=encode_multipart(data=input_patch_data, boundary=BOUNDARY),
            content_type=MULTIPART_CONTENT,
        )

        self.assertTrue(status.is_success(response.status_code))
        self.assertEqual(response.data["name"], new_name)

    def test_put(self):
        input_put_data = {
            "name": "media_name2",
            "file": ContentFile("test_file2", name="test_file2"),
            "type": "VIDEO",
            "search_target": self.search_target.id
        }
        response = self.client.put(
            f"{self.endpoint}{str(self.media.id)}/",
            data=encode_multipart(data=input_put_data, boundary=BOUNDARY),
            content_type=MULTIPART_CONTENT,
        )

        self.assertTrue(status.is_success(response.status_code))
        self.assertEqual(response.data["name"], input_put_data["name"])

    def test_delete(self):
        response = self.client.delete(f"{self.endpoint}{str(self.media.id)}/")
        self.assertTrue(status.is_success(response.status_code))
        with self.assertRaises(ObjectDoesNotExist):
            Media.objects.get(pk=self.media.id)
