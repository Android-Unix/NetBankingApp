from django.shortcuts import render
from django.http import HttpResponse
from rest_framework import viewsets , generics
from rest_framework.response import Response
from NetBanking.Service.service import (
    listUsers ,
    create_User ,
    getUserDetails ,
    delete_users ,
    listAccount ,
    createAccount
)
from NetBanking.models import Users
from NetBanking.serialize import UserSerializer
# Create your views here.

def homePage(request):
    return HttpResponse("Home")


class UserViewSet(viewsets.ViewSet) :
    def list(self , request) :
        return Response(listUsers().data)

    def retrieve_user(self , request , pk) :
        return Response(getUserDetails(pk).data)

    def delete_user(self , request , pk) :
        return Response(delete_users(pk) + " deleted successfully!")

class CreateUserViewSet(viewsets.ViewSet , generics.GenericAPIView) :
    queryset = Users.objects.all()
    serializer_class = UserSerializer

    def post(self , request) :
        return Response(create_User(request.data))


class AccountViewSet(viewsets.ViewSet) :

    def list_accounts(self , request , pk) :
        return Response(listAccount(pk).data)

    def create_account(self , request ,pk) :
        return createAccount(pk , request.data)
