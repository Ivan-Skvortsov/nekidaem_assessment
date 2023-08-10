import pytest

from apps.blogs.serializers import PostReadSerializer
from tests.test_01_posts import VALID_RESPONSE_POST_FIELDS

FEED_ENDPOINT = "/api/v1/feed/"


@pytest.mark.django_db(transaction=True)
def test_get_feed(authorized_client_2, test_posts, test_user_1, test_user_2):
    test_user_2.follows.add(test_user_1.blog)

    response = authorized_client_2.get(FEED_ENDPOINT)
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
def test_seen_posts_not_in_feed(authorized_client_2, test_posts, test_user_1, test_user_2):
    test_user_2.follows.add(test_user_1.blog)
    test_user_2.seen_posts.add(test_posts[0])
    response = authorized_client_2.get(FEED_ENDPOINT)
    assert response.status_code != 404
    assert response.status_code == 200

    data = response.json()
    assert data["count"] == len(test_posts) - 1

    assert test_posts[0].title not in data["results"]


@pytest.mark.django_db(transaction=True)
def test_deleted_posts_not_in_feed(authorized_client_2, test_posts, test_user_1, test_user_2):
    test_user_2.follows.add(test_user_1.blog)
    len_posts = len(test_posts)
    test_posts[0].delete()
    response = authorized_client_2.get(FEED_ENDPOINT)
    assert response.status_code != 404
    assert response.status_code == 200

    data = response.json()
    assert data["count"] == len_posts - 1

    assert test_posts[0].title not in data["results"]


@pytest.mark.django_db(transaction=True)
def test_unfollowed_blogs_not_in_feed(authorized_client_2, test_posts, test_user_1, test_user_2):
    test_user_2.follows.add(test_user_1.blog)
    response = authorized_client_2.get(FEED_ENDPOINT)
    assert response.status_code != 404
    assert response.status_code == 200

    data = response.json()
    assert data["count"] == len(test_posts)

    test_user_2.follows.remove(test_user_1.blog)
    response = authorized_client_2.get(FEED_ENDPOINT)
    assert response.status_code != 404
    assert response.status_code == 200

    data = response.json()
    assert data["count"] == 0
