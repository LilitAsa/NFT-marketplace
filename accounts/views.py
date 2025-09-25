from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.hashers import make_password
from .models import User
from .serializers import UserSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def perform_create(self, serializer):
        serializer.save(password=make_password(self.request.data['password']))