from django.apps import AppConfig


class FakeDbDataConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.fake_db_data"
