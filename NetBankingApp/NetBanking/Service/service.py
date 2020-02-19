
from NetBanking.models import Users , Account
from NetBanking.serialize import UserSerializer , AccountSerializer
from rest_framework.response import Response
from random import randint

def create_User(userdata) :
    serialize = UserSerializer(data = userdata)
    if serialize.is_valid() :
        serialize.save()
        return serialize.data
    else :
        return serialize.errors


def listUsers():
    queryset = Users.objects.all()
    return UserSerializer(queryset , many = True)

def getUserDetails(pk) :
    user = Users.objects.get(pk=pk)
    return UserSerializer(user)

def delete_users(pk):
    user = Users.objects.get(pk=pk)
    username = user.username
    user.delete()
    return username

def accountNumberGenerater() :
    return randint(10000000 , 99999999)

def createAccount(pk , pin):
    if Users.objects.get(pk=pk).accounts.count() <= 3 :
        accountdata = Account.objects.create(user=Users.objects.get(pk=pk) , pin=pin['pin'] , account_no = accountNumberGenerater(), balance=2000.00)
        data = AccountSerializer(accountdata)
        return Response({"status": "Created", "data": data.data})
    else :
        return Response(" Cannot have more than 3 accounts ..!!")


def listAccount(user) :
    account = Users.objects.get(pk=user).accounts.all()
    return AccountSerializer(account , many = True)
