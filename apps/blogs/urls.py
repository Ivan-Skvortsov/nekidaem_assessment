from django.urls import include, path
from rest_framework import routers

from apps.blogs import views

router = routers.DefaultRouter()
router.register("posts", views.PostViewSet)

urlpatterns = [path("", include(router.urls))]
