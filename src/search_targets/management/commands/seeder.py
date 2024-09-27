from datetime import datetime
import json
from pathlib import Path

from django.core.management.base import BaseCommand
from django.core.files import File

from search_targets.models import Media, SearchTarget, URL


# Location of seed data
DATA_FOLDER = Path(Path(__file__).parent, "data")
MEDIA_FOLDER = Path(DATA_FOLDER, "media")


class Command(BaseCommand):
    help = "Seed database for testing and development."

    def handle(self, *args, **options):
        create_seed_data()


def create_seed_data():
    """ Create seed data in database from local data """
    with open(Path(DATA_FOLDER, "search_targets.json"), "r") as file:
        data = json.load(file)
        for search_target_data in data:
            current_time = datetime.now()
            search_target = SearchTarget(
                search_text=search_target_data["search_text"],
                insertion_date=str(current_time.date()),
                insertion_time=str(current_time.time()),
                origin=search_target_data["origin"],
                original_url=search_target_data["original_url"],
            )
            search_target.save()

            for media_data in search_target_data["medias"]:
                local_media_file = open(str(Path(MEDIA_FOLDER, media_data["filename"])), "rb")
                django_media_file = File(local_media_file)
                media = Media(
                    search_target=search_target,
                    name=media_data["name"],
                    file=django_media_file,
                    type=media_data["type"]
                )
                media.save()

            for url in search_target_data["urls"]:
                db_url = URL(
                    search_target=search_target,
                    url=url
                )
                db_url.save()
