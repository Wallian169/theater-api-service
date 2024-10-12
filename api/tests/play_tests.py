from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from api.models import (
    Play,
    Performance,
    TheatreHall, Genre, Actor,
)
from api.serializers import PlayListDetailSerializer

PLAY_URL = reverse("api:play-list")
PERFORMANCE_URL = reverse("api:performance-list")


def sample_play(**params):
    defaults = {
        "name": "Sample play",
        "description": "Sample description",
    }
    defaults.update(params)

    return Play.objects.create(**defaults)


def sample_performance(**params):
    theatre_hall = TheatreHall.objects.create(
        "Blue", rows=20, seats_in_row=20
    )
    defaults = {
        "show_time": "2024-09-24 14:00",
        "play": sample_play(),
        "theatre_hall": theatre_hall,
    }
    defaults.update(params)

    return Performance.objects.create(**defaults)


def poster_upload_url(performance_id):
    return reverse("api:performance-upload-image", args=performance_id)


class UnauthenticatedPlayTest(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_auth_play(self):
        response = self.client.get(PLAY_URL)
        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED
        )


class AuthenticatedPlayTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            "user@theatre.com",
            "pass24word"
        )
        self.client.force_authenticate(self.user)

    def test_list_play(self):
        sample_play()
        sample_play()

        response = self.client.get(PLAY_URL)

        plays = Play.objects.order_by("id")
        serializer = PlayListDetailSerializer(plays, many=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_filter_by_genres_and_actors(self):
        # Setup genres and actors
        genre_1 = Genre.objects.create(name="Genre_1")
        genre_2 = Genre.objects.create(name="Genre_2")
        actor_1 = Actor.objects.create(
            first_name="first_name",
            last_name="last_name",
        )
        actor_2 = Actor.objects.create(
            first_name="first_name",
            last_name="last_name",
        )

        # Setup plays
        play_1 = sample_play(name="Sample play 1")
        play_1.genres.add(genre_1)
        play_1.actors.add(actor_1)

        play_2 = sample_play(name="Sample play 2")
        play_2.genres.add(genre_2)
        play_2.actors.add(actor_2)

        play_3 = sample_play(name="Play without genres or actors")

        # Make the GET request for both genres and actors
        response = self.client.get(
            PLAY_URL, {"genres": f"{genre_1.id},{genre_2.id}",
                       "actors": f"{actor_1.id},{actor_2.id}"}
        )

        # Serialize plays
        serializer1 = PlayListDetailSerializer(play_1)
        serializer2 = PlayListDetailSerializer(play_2)
        serializer3 = PlayListDetailSerializer(play_3)

        # Assertions
        self.assertIn(serializer1.data, response.data)
        self.assertIn(serializer2.data, response.data)
        self.assertNotIn(serializer3.data, response.data)

    def test_create_play_forbidden(self):
        payload = {
            "name": "Movie",
            "description": "Description",
        }
        res = self.client.post(PLAY_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)


class   AdminPlayTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_superuser(
            "user@theatre.com",
            "pass24word"
        )
        self.client.force_authenticate(self.user)

    def test_create_play(self):
        actor_1 = Actor.objects.create(
            first_name="First",
            last_name="Last",
        )

        genre_1 = Genre.objects.create(
            name="Genre_1"
        )

        payload = {
            "name": "Sample play",
            "description": "Sample description",
            "genres": [genre_1.id],
            "actors": [actor_1.id],
        }

        res = self.client.post(PLAY_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        play = Play.objects.get(id=res.data["id"])

        for key in payload.keys():
            if key in ["genres", "actors"]:
                related_ids = list(
                    getattr(play, key).values_list("id", flat=True))
                self.assertEqual(payload[key], related_ids)
            else:
                self.assertEqual(payload[key], getattr(play, key))
