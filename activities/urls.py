from django.urls import path
from rest_framework import routers

from activities.views import ActivityViewSet

router = routers.DefaultRouter()
router.register("", ActivityViewSet, basename="activities")

urlpatterns = []

urlpatterns += router.urls
