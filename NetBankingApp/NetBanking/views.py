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
    createAccount ,
    listTransactions ,
    accountDetails ,
    deleteAccount ,
    action ,
    transfer ,
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

    def account_details(self , request , pk , account_no) :
        return Response(accountDetails(pk , account_no).data)

    def delete_account(self , request , pk , account_no) :
        return Response(str(deleteAccount(pk , account_no)) + " Deleted Successfully")

    def bankAction(self , request , pk , account_no) :
        state = str(request.data['state'])
        money = int(request.data['money'])

        if state == 'w' or state == 'd' :
            return action(pk , account_no , money , state)
        else :
            return Response("Invalid action ..")

class TransationsViewSet(viewsets.ViewSet) :

    def list_transactions(self , request) :
        return listTransactions()

    def transferMoney(self , request , pk , account_no) :
        money=int(request.data['money'])
        receivers_account_no = int(request.data['receivers_account_no'])

        if not account_no == receivers_account_no :
            return transfer(pk , account_no , money , receivers_account_no)

        else :
            return Response(" Cannot tranfer money to same account as senders..!")
