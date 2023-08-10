import logging

import factory
from django.core.management.base import BaseCommand, CommandError

from apps.fake_db_data import factories

logging.basicConfig(
    format="%(asctime)s - [%(levelname)s] - %(message)s", level=logging.INFO, handlers=[logging.StreamHandler()]
)
logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = (
        "Заполняет БД тестовыми (фейковыми) данными. Заполнение возможно только на пустой базе данных. "
        "Если в БД присутствуют данные, сначала необходимо их удалить, выполнив команду `python manage.py flush`"
    )

    def add_arguments(self, parser):
        parser.add_argument(
            "--users",
            type=int,
            help="Количество пользователей",
        )
        parser.add_argument(
            "--posts",
            type=int,
            help="Количество постов",
        )

    def handle(self, *args, **options):
        num_users = options.get("users") or 100
        num_posts = options.get("posts") or 1000
        try:
            with factory.Faker.override_default_locale("ru_RU"):
                logger.info("Создание пользователей и блогов...")
                factories.UserFactory.create_batch(num_users)
                logger.info("Создание постов...")
                factories.PostFactory.create_batch(num_posts)
                logger.info("Создание подписок пользователей...")
                factories.create_random_subscriptions_for_users()
                logger.info("Создание просмотренных постов пользователей...")
                factories.create_random_seen_posts_for_users()
                logger.info("Создание фейковых данных завершено.")
        except CommandError as err:
            logger.info(f"Ошибка наполнения базы данных:\n{err}")
