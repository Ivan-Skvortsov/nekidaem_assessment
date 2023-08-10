import pytest

from apps.blogs.models import Post


@pytest.fixture
def guest_client():
    from rest_framework.test import APIClient

    return APIClient()


@pytest.fixture
def test_user_1(django_user_model):
    user_data = {
        "email": "user@example.com",
        "username": "@username",
        "first_name": "Вася",
        "last_name": "Пупкин",
        "password": "SomePassword123",
    }
    return django_user_model.objects.create(**user_data)


@pytest.fixture
def test_user_2(django_user_model):
    user_data = {
        "email": "user2@example.com",
        "username": "@username2",
        "first_name": "Петя",
        "last_name": "Курочкин",
        "password": "SomePassword123",
    }
    return django_user_model.objects.create(**user_data)


@pytest.fixture
def authorized_client_1(test_user_1):
    from rest_framework.authtoken.models import Token
    from rest_framework.test import APIClient

    token = Token.objects.get_or_create(user=test_user_1)[0]
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION="Token " + token.key)
    return client


@pytest.fixture
def valid_post_data():
    return {"title": "Заголовок поста", "text": "Текст поста"}


@pytest.fixture
def test_posts(test_user_1):
    Post.objects.create(title="Title", text="Text", blog=test_user_1.blog)
    Post.objects.create(title="Title2", text="Text2", blog=test_user_1.blog)
    Post.objects.create(title="Title3", text="Text3", blog=test_user_1.blog)
    return Post.objects.all()


# @pytest.fixture
# def valid_user_data():
#     return {
#         'email': 'user3@example.com',
#         'username': '@username3',
#         'first_name': 'Мистер',
#         'last_name': 'Икс',
#         'password': 'SomePassword123'
#     }
