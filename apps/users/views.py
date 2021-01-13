# Create your views here.
from rest_framework.generics import CreateAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from . import serializer
from django.contrib.auth.models import User

class RegisterView(CreateAPIView):

    serializer_class = serializer.RegisterSerializer



class UsernameValidateView(APIView):
    def get(self, request, username):
        data_dict = {
            "username": username,
            "count": User.objects.filter(username=username).count()
        }
        return Response(data_dict)


class EmailValidateView(APIView):
    def get(self, request, email):
        data_dict = {
            "email": email,
            "count": User.objects.filter(email=email).count()
        }
        return Response(data_dict)


