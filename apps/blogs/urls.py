from django.urls import include, path
from rest_framework import routers

from apps.blogs import views

router = routers.DefaultRouter()
router.register("posts", views.PostViewSet)
router.register("blogs", views.BlogViewSet)
router.register("feed", views.FeedViewSet, basename="feed")


urlpatterns = [path("", include(router.urls))]
