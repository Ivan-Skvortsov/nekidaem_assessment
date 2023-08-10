import pytest

BLOGS_ENDPOINT = "/api/v1/blogs/"


@pytest.mark.django_db(transaction=True)
def test_follow_blog_not_allowed_to_guests(guest_client, test_user_2):
    endpoint = f"{BLOGS_ENDPOINT}{test_user_2.blog.id}/follow/"
    response = guest_client.post(endpoint)

    assert response.status_code != 404
    assert response.status_code == 401


@pytest.mark.django_db(transaction=True)
def test_authorized_user_can_follow_blog(authorized_client_1, test_user_1, test_user_2):
    endpoint = f"{BLOGS_ENDPOINT}{test_user_2.blog.id}/follow/"
    response = authorized_client_1.post(endpoint)

    assert response.status_code != 404
    assert response.status_code == 201

    assert test_user_2.blog in test_user_1.follows.all()


@pytest.mark.django_db(transaction=True)
def test_authorized_user_can_not_follow_himself(authorized_client_1, test_user_1, test_user_2):
    endpoint = f"{BLOGS_ENDPOINT}{test_user_1.blog.id}/follow/"
    response = authorized_client_1.post(endpoint)

    assert response.status_code != 404
    assert response.status_code == 400

    assert test_user_1.blog not in test_user_1.follows.all()


@pytest.mark.django_db(transaction=True)
def test_authorized_user_can_unfollow_blog(authorized_client_1, test_user_1, test_user_2):
    test_user_1.follows.add(test_user_2.blog)
    endpoint = f"{BLOGS_ENDPOINT}{test_user_2.blog.id}/unfollow/"
    response = authorized_client_1.post(endpoint)

    assert response.status_code != 404
    assert response.status_code == 204

    assert test_user_2.blog not in test_user_1.follows.all()


@pytest.mark.django_db(transaction=True)
def test_authorized_user_can_not_unfollow_blog_he_is_not_following(authorized_client_1, test_user_1, test_user_2):
    endpoint = f"{BLOGS_ENDPOINT}{test_user_2.blog.id}/unfollow/"
    response = authorized_client_1.post(endpoint)

    assert response.status_code != 404
    assert response.status_code == 400
