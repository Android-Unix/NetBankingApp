import re
from rest_framework import serializers
from apps.NetBanking.models import Users , Account , Transactions
from django.core.validators import RegexValidator
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer) :
    class Meta:
        model = Users
        fields = [
            'id' ,
            'First_name' ,
            'Last_name' ,
            'username' ,
            'DOB' ,
            'Address' ,
            'password' ,
        ]


    def validate_First_name(self , firstname) :
        if  firstname == "" :
            raise serializers.ValidationError("First name needed..please enter correct first name ")

        return firstname

    def validate_Last_name(self , lastname) :
        if lastname == "" :
            raise serializers.ValidationError("Last name needed..please enter correct last name ")

        return lastname

    def validate_username(self , username) :
        if username == "" :
            raise serializers.ValidationError(" Unique Username needed boss.. ")

        else :
            validators=[
                RegexValidator(
                    r'^[\w.@+-]+$',
                    _('Enter a valid username. '
                        'This value may contain only letters, numbers '
                        'and @/./+/-/_ characters.'), 'invalid'),
            ],
            error_messages={
                'unique': _("A user with that username already exists."),
            }
        return username

    def validate_DOB(self, dob) :
        today = dob.today()
        diff = today - dob
        age = diff.days / 365
        if (age < 18):
            raise serializers.ValidationError("You are no eligible to have a bank account..so cannot create user account ")
        return dob

    def validate_password(self , password) :
        if password == "":
            raise serializers.ValidationError("Enter password ")

        else :
            if (len(password)<8):
                raise serializers.ValidationError("Password length must be minimum 8 characters")

            elif not re.search("[a-z]", password):
                raise serializers.ValidationError("password should contain atleatone lowercase letters")

            elif not re.search("[A-Z]", password):
                raise serializers.ValidationError(" password must contain atleast one UpperCase letter")

            elif not re.search("[0-9]", password):
                raise serializers.ValidationError(" password must contain atleast one digit [0 - 9]")

            elif not re.search("[_@$^&*!#]", password):
                raise serializers.ValidationError(" password must contain atleast one special character ")

        return password


class AccountSerializer(serializers.ModelSerializer) :

    class Meta:
        model = Account
        fields = [
            'user' ,
            'account_no' ,
            'pin' ,
            'balance' ,
        ]


    def validate_pin(self , pin) :
        if pin == "":
            raise serializers.ValidationError("Enter pin (Pin must only contain numbers) ")

        else :
            if int(len(str(pin))) <= 4:
                raise serializers.ValidationError("Pin length must be minimum 4 digits")

        return pin

    def create(self, validated_data):
        return Account.objects.create(**validated_data)

    def update(self, instance, validated_data):

        instance.user = validated_data.get('user', instance.user)
        instance.account_no = validated_data.get('account_no', instance.account_no)
        instance.pin = validated_data.get('pin', instance.pin)
        instance.balance = validated_data.get('balance', instance.balance)
        instance.save()
        return instance


class TransationsSerializer(serializers.ModelSerializer) :
    class Meta:
        model = Transactions
        fields = [
                'senders' ,
                'receivers' ,
                'moneysent' ,
                ]
        depth = 1
