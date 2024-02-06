from django.contrib import admin
from .models import Bankuser, Recipient, Transaction

# Register your models here.
class TransactionAdmin(admin.ModelAdmin):
    list_display = ['bankuser', 'recipient', 'transaction_id']

class BankuserAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'account_number')
    #prepopulated_fields = {'slug': ('first_name',)}
admin.site.register(Bankuser, BankuserAdmin)
admin.site.register(Recipient)
admin.site.register(Transaction, TransactionAdmin)
