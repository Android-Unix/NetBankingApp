from django.contrib import admin
from apps.NetBanking.models import Users , Account , Transactions

# Register your models here.
admin.site.register(Users)
admin.site.register(Account)
admin.site.register(Transactions)
