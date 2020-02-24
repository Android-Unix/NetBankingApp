from django.shortcuts import render
from django.http import HttpResponse
from rest_framework import viewsets, generics
from rest_framework.response import Response
from apps.NetBanking.Service.service import (
    UserHelperService,
    AccountHelperService,
    TransactionHelperService,
)

from apps.NetBanking.models import Users, Account
from apps.NetBanking.serializer import UserSerializer
# Create your views here.

def homePage(request):
    return HttpResponse("Home")


class UserViewSet(viewsets.ViewSet):
    def list(self, request):
        return UserHelperService.listUsers()

    def retrieve_user(self, request, pk):
        return UserHelperService.getUserDetails(pk)

    def delete_user(self, request, pk):
        return UserHelperService.delete_users(pk)

class CreateUserViewSet(viewsets.ViewSet, generics.GenericAPIView):
    queryset = Users.objects.all()
    serializer_class = UserSerializer

    def post(self, request):
        return UserHelperService.create_User(request.data)


class AccountViewSet(viewsets.ViewSet):

    def list_accounts(self, request, pk):
        return AccountHelperService.listAccount(pk)

    def create_account(self, request ,pk):
        return AccountHelperService.createAccount(pk, request.data)

    def account_details(self, request, pk, account_id):
        return AccountHelperService.accountDetails(pk, account_id)

    def delete_account(self, request, pk, account_id):
        return AccountHelperService.deleteAccount(pk, account_id)

    def bankAction(self, request, pk, account_id):
        state = str(request.data['state'])
        money = int(request.data['money'])

        if state == 'w' or state == 'd':
            return TransactionHelperService.action(pk, account_id, money, state)
        else:
            return Response("Invalid action ..")

class TransationsViewSet(viewsets.ViewSet):

    def list_transactions(self, request):
        return TransactionHelperService.listTransactions()

    def transferMoney(self, request, pk, senders_account_id):
        money=int(request.data['money'])
        receivers_account_no = int(request.data['receivers_account_no'])

        if not Account.objects.get(pk=senders_account_id).account_no == receivers_account_no :
            return TransactionHelperService.transfer(pk, senders_account_id, money, receivers_account_no)

        else :
            return Response(" Cannot tranfer money to same account as senders..!")
