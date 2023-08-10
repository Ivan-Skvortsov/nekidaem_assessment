import pytest

from apps.blogs.models import Post
from apps.blogs.serializers import PostReadSerializer

POSTS_ENDPOINT = "/api/v1/posts/"


VALID_RESPONSE_POST_FIELDS = ["id", "title", "text", "created_at", "blog"]

VALID_REQUEST_POST_FIELDS = ["title", "text"]


@pytest.mark.django_db(transaction=True)
def test_get_all_posts(guest_client, test_posts):
    response = guest_client.get(POSTS_ENDPOINT)
    assert response.status_code != 404
    assert response.status_code == 200

    # pagination
    data = response.json()
    assert "count" in data
    assert data["count"] == len(test_posts)
    assert "next" in data
    assert "previous" in data
    assert "results" in data

    # fields
    assert type(data["results"]) == list
    assert set(data["results"][0]) == set(VALID_RESPONSE_POST_FIELDS)

    # data
    serializer = PostReadSerializer(test_posts, many=True)
    assert data["results"] == serializer.data


@pytest.mark.django_db(transaction=True)
def test_create_post_not_allowed_to_guests(guest_client):
    response = guest_client.post(POSTS_ENDPOINT)

    assert response.status_code != 404
    assert response.status_code == 401
    assert not Post.objects.all().exists()


@pytest.mark.django_db(transaction=True)
def test_create_post_empty_data(authorized_client_1):
    response = authorized_client_1.post(POSTS_ENDPOINT)

    assert response.status_code != 404
    assert response.status_code == 400

    for field in VALID_REQUEST_POST_FIELDS:
        assert field in response.json()

    assert not Post.objects.all().exists()


@pytest.mark.django_db(transaction=True)
def test_create_post_invalid_data(authorized_client_1):
    response = authorized_client_1.post(POSTS_ENDPOINT, {"bla": "bla"}, format="json")

    assert response.status_code != 404
    assert response.status_code == 400

    assert not Post.objects.all().exists()


@pytest.mark.django_db(transaction=True)
def test_create_post_valid_data(authorized_client_1, valid_post_data):
    response = authorized_client_1.post(POSTS_ENDPOINT, valid_post_data, format="json")

    assert response.status_code != 404
    assert response.status_code == 201

    recipe = Post.objects.all()
    assert recipe.exists()
    assert recipe.count() == 1


@pytest.mark.django_db(transaction=True)
def test_user_can_mark_post_as_seen(authorized_client_1, test_user_1, test_posts):
    endpoint = f"{POSTS_ENDPOINT}{test_posts[0].id}/seen/"
    response = authorized_client_1.post(endpoint)

    assert response.status_code != 404
    assert response.status_code == 201

    assert test_posts[0] in test_user_1.seen_posts.all()


@pytest.mark.django_db(transaction=True)
def test_guest_user_can_not_mark_post_as_seen(guest_client, test_posts):
    endpoint = f"{POSTS_ENDPOINT}{test_posts[0].id}/seen/"
    response = guest_client.post(endpoint)

    assert response.status_code != 404
    assert response.status_code == 401
