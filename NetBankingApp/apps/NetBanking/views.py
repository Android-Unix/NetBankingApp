from django.shortcuts import render
from django.http import HttpResponse
from rest_framework import viewsets , generics
from rest_framework.response import Response
from apps.NetBanking.Service.service import (
    UserHelperService,
    AccountHelperService ,
    TransactionHelperService ,
)

from apps.NetBanking.models import Users
from apps.NetBanking.serialize import UserSerializer
# Create your views here.

def homePage(request):
    return HttpResponse("Home")


class UserViewSet(viewsets.ViewSet) :
    def list(self , request) :
        return UserHelperService.listUsers()

    def retrieve_user(self , request , pk) :
        return UserHelperService.getUserDetails(pk)

    def delete_user(self , request , pk) :
        return Response(UserHelperService.delete_users(pk) + " deleted successfully!")

class CreateUserViewSet(viewsets.ViewSet , generics.GenericAPIView) :
    queryset = Users.objects.all()
    serializer_class = UserSerializer

    def post(self , request) :
        return UserHelperService.create_User(request.data)


class AccountViewSet(viewsets.ViewSet) :

    def list_accounts(self , request , pk) :
        return AccountHelperService.listAccount(pk)

    def create_account(self , request ,pk) :
        return AccountHelperService.createAccount(pk , request.data)

    def account_details(self , request , pk , account_no) :
        return AccountHelperService.accountDetails(pk , account_no)

    def delete_account(self , request , pk , account_no) :
        return Response(str(AccountHelperService.deleteAccount(pk , account_no)) + " Deleted Successfully")

    def bankAction(self , request , pk , account_no) :
        state = str(request.data['state'])
        money = int(request.data['money'])

        if state == 'w' or state == 'd' :
            return TransactionHelperService.action(pk , account_no , money , state)
        else :
            return Response("Invalid action ..")

class TransationsViewSet(viewsets.ViewSet) :

    def list_transactions(self , request) :
        return TransactionHelperService.listTransactions()

    def transferMoney(self , request , pk , account_no) :
        money=int(request.data['money'])
        receivers_account_no = int(request.data['receivers_account_no'])

        if not account_no == receivers_account_no :
            return TransactionHelperService.transfer(pk , account_no , money , receivers_account_no)

        else :
            return Response(" Cannot tranfer money to same account as senders..!")
