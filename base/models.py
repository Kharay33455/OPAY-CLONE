from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Bankuser(models.Model):
    first_name = models.CharField(max_length = 20)
    last_name = models.CharField(max_length = 20)
    balance = models.IntegerField(default = 9999999)
    transfer_pin = models.CharField(max_length = 4)
    account_owner = models.OneToOneField(User, on_delete = models.SET_NULL, null = True)
    account_number = models.IntegerField(unique = True)
    money_out = models.BigIntegerField(default = 0)
    money_in = models.BigIntegerField(default = 0)
    slug = models.SlugField(max_length = 225, null = True, blank = True ,unique = True)


    def __str__(self):
        """function to return defining factor"""
        return f'{self.first_name} {self.last_name}'

class Recipient(models.Model):
    bankuser = models.ForeignKey(Bankuser, on_delete = models.CASCADE)
    first_name = models.CharField(max_length = 20)
    last_name = models.CharField(max_length = 20)
    account_number = models.IntegerField()
    no_of_transfers = models.IntegerField(default = 0)
    last_transfer = models.DateTimeField(auto_now = True)

    def __str__(self):
        return self.first_name
    
    def get_recipient_account(self):
        return self.account_number
    
class Transaction(models.Model):
    bankuser = models.ForeignKey(Bankuser, on_delete = models.CASCADE)
    recipient = models.ForeignKey(Recipient, on_delete = models.CASCADE)
    amount = models.IntegerField()
    time_of_transfer = models.DateTimeField(auto_now_add = True)
    transaction_id = models.IntegerField(unique = True)


    def __str__(self):
        return f'{self.bankuser.first_name} transfer to {self.recipient.first_name} on {self.time_of_transfer}'
