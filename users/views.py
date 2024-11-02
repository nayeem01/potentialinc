# users/views.py
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

from .serializers import RegisterSerializer


class RegisterUserView(APIView):
    """
    Endpoint to register a new user.
    """

    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "User created successfully"}, status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    """
    Custom login view to support both Username/Password and Email/Password.
    """

    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        identifier = request.data.get("identifier")
        password = request.data.get("password")

        if not identifier or not password:
            return JsonResponse(
                {"error": "Please provide both identifier and password."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        user = authenticate(request, username=identifier, password=password)
        if not user:
            try:
                user_obj = User.objects.get(email=identifier)
                user = authenticate(
                    request, username=user_obj.username, password=password
                )
            except User.DoesNotExist:
                user = None

        if user:
            refresh = RefreshToken.for_user(user)
            return JsonResponse(
                {
                    "refresh": str(refresh),
                    "access": str(refresh.access_token),
                }
            )
        else:
            return JsonResponse(
                {"error": "Invalid credentials."},
                status=status.HTTP_401_UNAUTHORIZED,
            )
