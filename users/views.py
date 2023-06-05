from django.contrib.auth import get_user_model
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from users.serializers import CustomUserDetailsSerializer

UserModel = get_user_model()


class UserView(ModelViewSet):
    permission_classes = (IsAuthenticated,)
    queryset = UserModel.objects.all()
    serializer_class = CustomUserDetailsSerializer

    @action(detail=False)
    def me(self, request):
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)
