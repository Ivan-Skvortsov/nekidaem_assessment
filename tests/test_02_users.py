import pytest

from apps.blogs.models import Blog


@pytest.mark.django_db(transaction=True)
def test_blogs_added_when_user_created(test_user_1):
    blogs = Blog.objects.all()
    assert blogs.count() == 1
    assert test_user_1.blog in blogs
