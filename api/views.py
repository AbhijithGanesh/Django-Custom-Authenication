from django.shortcuts import render
from rest_framework import generics
from rest_framework.views import APIView
from django.contrib.auth.models import User
from rest_framework import permissions
from .serializers import *
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token


class Register(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = RegisterSerializer
    def get(self, request):
        return Response ( {"Message":"Enter Details to Get a Response"}, status = status.HTTP_204_NO_CONTENT)

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        token = Token.objects.get_or_create(user=serializer.instance)
        return Response(
            {
                "token": str(token[0]),
                "username": serializer.instance.username,
            },
            status=status.HTTP_201_CREATED,
        )


class Login(APIView):
    def get(self, request):
        return Response(    
            {"Message":"Enter Details to Get a Response"},
            status = status.HTTP_204_NO_CONTENT,
        )
    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        if not username or not password:
            return Response(
                {"error": "username or password not provided"},
                status=status.HTTP_422_UNPROCESSABLE_ENTITY,
            )

        user_obj = authenticate(username=username, password=password)

        if not user_obj:
            return Response(
                {"error": "username or password is incorrect"},
                status=status.HTTP_422_UNPROCESSABLE_ENTITY,
            )

        token = Token.objects.get_or_create(user=user_obj)
        return Response(
            {
                "detail": "Login Successful",
            },
            status=status.HTTP_200_OK,
        )
