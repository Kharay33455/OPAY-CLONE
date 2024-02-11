from django.shortcuts import render
from .models import Bankuser, Recipient, Transaction
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views.decorators.clickjacking import xframe_options_sameorigin
from django.db.models import F
import random
import string 
from django.utils import timezone
from django.shortcuts import get_object_or_404
from .forms import AccountNumberForm, AmountForm
from django.http import Http404
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest

# Create your views here.
def logged_out(request):
    context = {}
    return render(request, 'base/base.html', context)


@login_required
def home(request, slug):
    bankuser = Bankuser.objects.get(slug=slug)
    if bankuser.account_owner == request.user:
        balance = bankuser.balance
        

        balance = str(balance)
        cashback = balance[1:4]
        balance = f'{balance[0] + ","+ balance[1:4] + "," + balance[4:8]}'
        firstname = bankuser.first_name
        tell = request.__dict__
        context= {"balance":balance, "firstname":firstname, "bankuser": bankuser, "cashback": cashback}
        return render(request, 'base/opay.html', context)
    else:
        return HttpResponseRedirect(reverse('users:login'))

@login_required
def transfer(request, slug):
    bankuser = Bankuser.objects.get(slug=slug)
    context = {"bankuser": bankuser}
    return render(request, 'base/Transfer.html', context)


@login_required
def to_opay_account(request, slug):
    bankuser = Bankuser.objects.get(slug=slug)
    form = AccountNumberForm()
    context = {"bankuser": bankuser, "form" : form}
    return render(request, 'base/toopay.html', context)


@login_required
def transfer_operator(request, slug):
    bankuser= get_object_or_404(Bankuser, slug=slug)
    if request.method == "POST":
        form = AccountNumberForm(request.POST)
        #check if forms is valid 
        if form.is_valid():
            try:

            #process and get data
                account_number = form.cleaned_data['account_number']
                account_number = account_number
                recipient = bankuser.recipient_set.get(account_number = account_number)
                if recipient:
                    account_number = recipient.account_number

            #redirect to ammount url
                    return HttpResponseRedirect(reverse("base:tfamount", args=(slug, account_number)))
            except(KeyError, Recipient.DoesNotExist):
                firstname = ('Kharay', "Slai", "Cesana", "Bruce", "Aang", "Benjamin", "Mozilla", "Victor", "Peter", "Fay", "Benochi")
                lastname = ("Chinazamuepele", "Solon", "Micah", "Beast O' Javadan", "State", "Shallipoppi", "Zerry", "Ronaldo", "Buttercup", "Kingsley")
                first_name = random.choice(firstname)
                last_name = random.choice(lastname)
                new_account_number =account_number
                recipient = bankuser.recipient_set.create(first_name = first_name, last_name = last_name, account_number = new_account_number)
                return HttpResponseRedirect(reverse("base:tfamount", args=(slug, account_number)))

                
        else :
            form = AccountNumberForm()
            return render(request, 'base/invalid.html', {"form": form, "error_msg": "invalid shit"})

            


@login_required
@xframe_options_sameorigin
def recent_transactions(request, slug):
    bankuser = Bankuser.objects.get(slug = slug)
    recipient = bankuser.recipient_set.order_by("-last_transfer")
    context = {"bankuser": bankuser, "recipient": recipient}
    return render (request, 'base/recents.html', context)


@login_required
@xframe_options_sameorigin
def favorites_transactions(request, slug):
    bankuser = Bankuser.objects.get(slug = slug)
    recipient = bankuser.recipient_set.order_by("-no_of_transfers")
    context = {"bankuser": bankuser, "recipient": recipient}
    return render (request, 'base/favorites.html', context)


@login_required
def transfer_amount(request, slug, account_number):
    bankuser = Bankuser.objects.get(slug = slug)
    recipient = bankuser.recipient_set.get(account_number = account_number)
    form =  AmountForm()
    context = {"bankuser": bankuser, "recipient": recipient, "form": form}

    return render (request, 'base/transfer_amount.html', context)


@login_required
def amount_operator(request, slug, account_number):
    bankuser = Bankuser.objects.get(slug=slug)
    recipient = bankuser.recipient_set.get(account_number = account_number)
    account_number = recipient.account_number
    amount = request.POST['amount']
    context = {'bankuser': bankuser, 'recipient' : recipient, 'amount': amount, 'account_number': account_number}
    return render (request, 'base/transfer_amount.html', context)


@login_required
def transaction_operator(request, slug, account_number, amount):
    bankuser = Bankuser.objects.get(slug=slug)
    recipient = bankuser.recipient_set.get(account_number = account_number)
    account_number = recipient.account_number
    amount = amount 
    tf_pin = bankuser.transfer_pin
    tf_pin = int(tf_pin)
    pin = request.POST['pin']
    pin = int(pin)
    if pin == tf_pin:
        new_balance =  bankuser.balance - amount
        bankuser.balance = new_balance
        bankuser.save()
        t_id = random.randint(11111111, 99999999)
        t_id = str(t_id)
        acn = str(bankuser.account_number)
        t_id = f'{t_id + acn}'
        new_transaction = bankuser.transaction_set.create(recipient = recipient, amount = amount, time_of_transfer = timezone.now(), transaction_id = t_id )
        recipient.last_transfer = timezone.now()
        recipient.no_of_transfers = F("no_of_transfers") + 1
        recipient.save()

        context = {'bankuser': bankuser, 'account_number' : account_number, 'amount': amount, 'msg':'Transfer Succesful'}
        return render(request, 'base/invalid.html', context)
    else:
    

    

        context = {'bankuser': bankuser, 'account_number' : account_number, 'amount': amount, 'errmsg': 'invalid pin'}

        return render (request, 'base/invalid.html', context)


@login_required
def transaction_history(request, slug):
    bankuser = Bankuser.objects.get(slug=slug)
    transactions = bankuser.transaction_set.order_by('-time_of_transfer')
    context = {'bankuser': bankuser, "transactions": transactions}
    return render(request, 'base/transaction_history.html', context)


def transaction_details(request, slug, transaction_id):
    bankuser = Bankuser.objects.get(slug=slug)
    transaction = Transaction.objects.get(transaction_id = transaction_id)
    fee = transaction.amount
    fee = str(fee)
    fee = fee[0:2]
    context = {'bankuser': bankuser, 'transaction':transaction, 'fee': fee}
    return render(request, 'base/transaction_details.html', context)