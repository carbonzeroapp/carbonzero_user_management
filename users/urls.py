from django.urls import path, include
from rest_framework import routers

from users.views import UserView

router = routers.DefaultRouter()
router.register(r'', UserView, basename='user')

urlpatterns = [
    path('', include(router.urls)),
]
