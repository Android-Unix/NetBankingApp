from django.contrib import admin
from NetBanking.models import Users , Account , Transations

# Register your models here.
admin.site.register(Users)
admin.site.register(Account)
admin.site.register(Transations)
