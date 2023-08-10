from .settings import *  # noqa

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "NAME": "nekidaem_test_base",
        "USER": "test_postgres",
        "PASSWORD": "test_postgres",
        "HOST": "localhost",
        "PORT": 5438,
    }
}
