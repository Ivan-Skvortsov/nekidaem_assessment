from apps.blogs.models import Post
from apps.users.models import User


def get_posts_for_user_feed(user: User, limit: int):
    posts_from_followed_blogs = Post.objects.filter(blog__in=user.follows.all())
    seen_posts = user.seen_posts.all()
    return posts_from_followed_blogs.exclude(pk__in=seen_posts)[:limit]
