
from apps.NetBanking.models import Users , Account , Transactions
from apps.NetBanking.serializer import UserSerializer , AccountSerializer , TransationsSerializer
from rest_framework.response import Response
from apps.NetBanking.Utils.utils import accountNumberGenerater

class UserHelperService :

    def create_User(userdata) :
        serialize = UserSerializer(data = userdata)
        if serialize.is_valid() :
            serialize.save()
            return Response(serialize.data)
        else :
            return Response(serialize.errors)

    def listUsers():
        queryset = Users.objects.all()
        return Response(UserSerializer(queryset , many = True).data)

    def getUserDetails(pk) :
        user = Users.objects.get(pk=pk)
        return Response(UserSerializer(user).data)

    def delete_users(pk):
        user = Users.objects.get(pk=pk)
        username = user.username
        user.delete()
        return username

class AccountHelperService :

    def createAccount(pk , pin):
        if Users.objects.get(pk=pk).accounts.count() < 3 :
            accountdata = {
                "user" : Users.objects.get(pk=pk).pk ,
                "pin" : pin['pin'] ,
                "account_no" : accountNumberGenerater() ,
                "balance" : 2000.00
            }
            # accountdata = Account(user_id=pk , pin=pin['pin'] , account_no = accountNumberGenerater(), balance=2000.00)

            serializedaccount=AccountSerializer(data=accountdata)
            if serializedaccount.is_valid() :
                serializedaccount.save()
                return Response({"status": "Created", "data": serializedaccount.data})
            else :
                return Response({"error_messages:" : serializedaccount.errors})
        else :
            return Response(" Cannot have more than 3 accounts ..!!")


    def listAccount(user) :
        account = Users.objects.get(pk=user).accounts.all()
        return Response(AccountSerializer(account , many = True).data)

    def accountDetails(pk , account_no) :
        account = Users.objects.get(pk=pk).accounts.get(account_no=account_no)
        return Response(AccountSerializer(account).data)


    def deleteAccount(pk , account_no) :
        account = Users.objects.get(pk=pk).accounts.get(account_no=account_no)
        accountNo = account.account_no
        account.delete()
        return accountNo

class TransactionHelperService :

    def listTransactions() :
        serializedTransactiondata = TransationsSerializer(Transactions.objects.all() , many = True)
        return Response({ "transactionData" : serializedTransactiondata.data})


    def action(pk , account_no , money , state) :
        if state == 'w' :
            return withdraw(pk , account_no , money)

        if state == 'd' :
            return deposit(pk , account_no , money)


    def withdraw(pk , account_no , money) :
        account = Users.objects.get(pk=pk).accounts.get(account_no=account_no)
        if float(money) > account.balance:
            return Response(" Unsufficient balance ")
        elif account.balance <= 2000 :
            return Response(" Cannot withdraw money...Account balance less than mininum balance")
        elif account.balance - money <= 2000 :
            return Response(" Withdrawing this amount cause balance to go below minimum balance ..So cannot withdraw")
        else :
            account.balance -= money
            account.save()
            return Response(" successfully Withdrawed ")

    def deposit(pk , account_no , money) :
        account = Users.objects.get(pk=pk).accounts.get(account_no=account_no)
        if money < 0 :
            return Response(" Money doesnt exist boss!! ")

        else:
            account.balance += money
            account.save()
            return Response(" successfully Deposited ")

    def transfer(pk , sender_account_no , money , receivers_account_no) :
        senderaccount = Users.objects.get(pk=pk).accounts.get(account_no=sender_account_no)

        if senderaccount.balance <= 2000 :
            return Response(" Cannot transfer as balance is less than minimum balance")
        elif senderaccount.balance - money <= 2000 :
            return Response(" Cannot transfer as balance will become less than minimum balance after this transaction")
        else:
            try :
                receiveraccount = Account.objects.get(account_no=receivers_account_no)
            except (KeyError, Account.DoesNotExist):
                return Response(" Invalid Account Number")

            senderaccount.balance -= money
            senderaccount.save()

            receiveraccount.balance += money
            receiveraccount.save()

            tobj = Transactions.objects.create(senders = senderaccount , receivers = receiveraccount , moneysent = money)
            Response(TransationsSerializer(tobj , many = True))
            return Response(" Money sent successfully ")
