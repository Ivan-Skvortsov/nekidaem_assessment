import random

import factory

from apps.blogs.models import Blog, Post
from apps.users.models import User


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    username = factory.Sequence(lambda n: f"User-{n}")


class PostFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Post

    title = factory.Faker("text", max_nb_chars=100)
    text = factory.Faker("text", max_nb_chars=1000)
    blog = factory.Iterator(Blog.objects.all())


def __get_random_objects_by_model(model):
    random_objs_ids = __get_random_ids_by_model(model)
    return model.objects.filter(pk__in=random_objs_ids)


def __get_random_ids_by_model(model):
    all_obj_scount = model.objects.all().count()
    return random.choices(range(1, all_obj_scount), k=all_obj_scount // 5)


def create_random_seen_posts_for_users():
    random_users = __get_random_objects_by_model(User)
    for user in random_users:
        user.seen_posts.add(*__get_random_objects_by_model(Post))


def create_random_subscriptions_for_users():
    random_users = __get_random_objects_by_model(User)
    for user in random_users:
        user.follows.add(*__get_random_objects_by_model(Blog))
