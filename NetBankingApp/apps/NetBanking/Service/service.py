
from apps.NetBanking.models import Users, Account, Transactions , AccountTransaction
from apps.NetBanking.serializer import (
    UserSerializer,
    AccountSerializer,
    TransationsSerializer,
    AccountTransactionSerializer,
)
from rest_framework.response import Response
from apps.NetBanking.Utils.utils import accountNumberGenerater
from django.db.models import F
from datetime import datetime

class UserHelperService:

    def create_User(userdata):
        serialize = UserSerializer(data=userdata)
        if serialize.is_valid():
            serialize.save()
            return Response(serialize.data)
        else:
            return Response(serialize.errors)

    def listUsers():
        queryset = Users.objects.all()
        return Response(UserSerializer(queryset, many=True).data)

    def getUserDetails(pk):
        user = Users.objects.get(pk=pk)
        return Response(UserSerializer(user).data)

    def delete_users(pk):
        user = Users.objects.get(pk=pk)
        username = user.username
        user.delete()
        return Response(str(username) + " deleted Successfully")

class AccountHelperService:

    def createAccount(pk, pin):
        if Users.objects.get(pk=pk).accounts.count() < 3:
            accountdata = {
                "user": Users.objects.get(pk=pk).pk,
                "pin": pin['pin'],
                "account_no": accountNumberGenerater(),
                "balance": 2000.00
            }

            serializedaccount = AccountSerializer(data=accountdata)
            if serializedaccount.is_valid():
                serializedaccount.save()
                return Response({"status": "Created", "data": serializedaccount.data})
            else:
                return Response({"error_messages:": serializedaccount.errors})
        else:
            return Response(" Cannot have more than 3 accounts ..!!")


    def listAccount(user):
        account = Users.objects.get(pk=user).accounts.all()
        return Response(AccountSerializer(account, many=True).data)

    def accountDetails(pk, account_id):
        account = Users.objects.get(pk=pk).accounts.get(pk=account_id)
        return Response(AccountSerializer(account).data)


    def deleteAccount(pk, account_id):
        account = Users.objects.get(pk=pk).accounts.get(pk=account_id)
        accountNo = account.account_no
        account.delete()
        return Response(str(accountNo) + " Deleted Successfully!")

class TransactionHelperService:

    def listTransactions():
        serializedTransactiondata = TransationsSerializer(Transactions.objects.all(), many=True)
        return Response({"transactionData": serializedTransactiondata.data})


    def withdraw(pk, account_id, money):
        account = Account.objects.get(pk=account_id)
        if float(money) > account.balance:
            return Response(" Unsufficient balance ")
        elif account.balance <= 2000:
            return Response(" Cannot withdraw money...Account balance less than mininum balance")
        elif account.balance - money <= 2000:
            return Response(" Withdrawing this amount cause balance to go below minimum balance ..So cannot withdraw")
        else:

            data = {
                "moneywithdrawed": money,
                "active_account": account.pk
            }

            account.balance = F('balance') - money
            account.save()

            serializedata = AccountTransactionSerializer(data=data)
            if serializedata.is_valid():
                log_file = open("log.txt", "a+")
                log_file.write(str(serializedata.validated_data))
                log_file.write("\n")
                log_file.close()
                serializedata.save()
                return Response(serializedata.data)
            else:
                return Response(serializedata.errors)


    def deposit(pk, account_id, money):
        account = Account.objects.get(pk=account_id)
        if money < 0:
            return Response(" Money doesnt exist boss!! ")

        else:
            data = {
                "moneydeposited": money,
                "active_account": account.pk
            }
            account.balance = F('balance') + money
            account.save()

            serializedata = AccountTransactionSerializer(data=data)
            if serializedata.is_valid():
                log_file = open("log.txt", "a+")
                log_file.write(str(serializedata.validated_data))
                log_file.write("\n")
                log_file.close()
                serializedata.save()
                return Response(serializedata.data)
            else:
                return Response(serializedata.errors)

    def action(pk, account_id, money, state):
        if state == 'w':
            return TransactionHelperService.withdraw(pk, account_id, money)

        if state == 'd':
            return TransactionHelperService.deposit(pk, account_id, money)

    def transfer(pk, sender_account_id, money, receivers_account_no):
        senderaccount = Accounts.objects.get(pk=sender_account_id)

        if senderaccount.balance <= 2000:
            return Response(" Cannot transfer as balance is less than minimum balance")
        elif senderaccount.balance - money <= 2000:
            return Response(" Cannot transfer as balance will become less than minimum balance after this transaction")
        else:
            try:
                receiveraccount = Account.objects.get(account_no=receivers_account_no)
            except (KeyError, Account.DoesNotExist):
                return Response(" Invalid Account Number")

            senderaccount.balance = F('balance') - money
            senderaccount.save()

            receiveraccount.balance = F('balance') + money
            receiveraccount.save()

            tobj = Transactions.objects.create(senders=senderaccount, receivers=receiveraccount, moneysent=money)
            Response(TransationsSerializer(tobj, many=True))
            return Response(" Money sent successfully ")

    def list_account_activity(pk , account_id):
        accountactivity = AccountTransaction.objects.filter(active_account=account_id)
        log_file = open("log.txt", "a+")
        log_file.write(str(accountactivity))
        log_file.write("\n")
        log_file.write(str(AccountTransactionSerializer(accountactivity, many=True).data))
        log_file.write("\n")
        log_file.close()
        return Response(AccountTransactionSerializer(accountactivity, many=True).data)
