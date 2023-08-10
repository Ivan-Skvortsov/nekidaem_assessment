from celery import shared_task

from apps.blogs.serializers import PostReadSerializer
from apps.blogs.utils import get_posts_for_user_feed
from apps.users.models import User


@shared_task
def fake_send_email(user_id: int):
    user = User.objects.get(pk=user_id)
    posts = get_posts_for_user_feed(user=user, limit=5)
    if not posts:
        print(f"У пользователя {user} нет новых в ленте. Сообщение не отправлено.")
    else:
        serializer = PostReadSerializer(posts, many=True)
        message = {"Новые посты:": serializer.data}
        print(f"Отправлено сообщение пользователю {user}: {message}")


@shared_task
def send_emails_to_users():
    fake_send_email.chunks(
        ((user_id,) for user_id in User.objects.all().values_list("pk", flat=True)), n=100
    ).apply_async()
