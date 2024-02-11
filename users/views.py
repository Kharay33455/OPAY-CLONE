from django.shortcuts import render
from django.contrib.auth import login
from django.contrib.auth import logout
from django.contrib.auth import authenticate
from base.models import Bankuser
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.models import User
from django.http import Http404


# Create your views here.


def login_request(request):
        
    if request.method == 'POST':
        try:

            account_number = request.POST['account_number']
            password = request.POST['password']
            bankuser = Bankuser.objects.get(account_number = account_number)
            username = bankuser.account_owner
            slug = bankuser.slug
            user = authenticate(request, username = username, password = password)
            if user is not None:
                login(request, user) 
                return HttpResponseRedirect(reverse ('base:home', args=(slug,)))
            else:
                context = {'error_message': "Invalid account number or password"}
                return render(request, 'users/login.html', context)
        except(ValueError):
            context = {'error_message' : 'You didn\'t submit valid credentials'}
            return render(request, 'users/login.html', context)
        except(KeyError, Bankuser.DoesNotExist):
            context = {'error_message': "Invalid account number or password"}
            return render(request, 'users/login.html', context)
    else:
        context  = {}
        return render(request, 'users/login.html', context)


def registration_request(request):
    if request.method == 'POST':
        account_number = request.POST['account_number']
        password = request.POST['password']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        pin = request.POST['pin']
        if len(account_number) == 10 and len(password) == 6 and len(first_name) < 20 and len(last_name)< 20 and len(pin) == 4:
            user_new = User.objects.create_user(username = account_number, email = 'dummyemail@gmail.com', first_name = request.POST['first_name'], last_name = request.POST['last_name'], password = request.POST['password'])
            user_new.save()
            slugger = f'{first_name.lower() + "-"+last_name.lower()}'
            counter = 1
            while Bankuser.objects.filter(slug = slugger).exists():
                slugge = f'{first_name.lower() + "-" + last_name.lower()}'
                slugger = f'{slugge}-{counter}'
                counter +=1
                

            slip = slugger
            new_user = Bankuser.objects.create(first_name = first_name, last_name = last_name, transfer_pin = pin, account_owner = user_new, account_number = account_number, slug = slip)
            #authenticate and log in user
            authenticated_user = authenticate(request, username = user_new.username, password = request.POST['password'])
            login(request, authenticated_user)
            if authenticated_user.is_authenticated:
                bankuser = Bankuser.objects.get(account_number = account_number)
                slug = bankuser.slug
                return HttpResponseRedirect(reverse('base:home', args=(slug,)))
            else:
                raise Http404("AUthentications error")
        else:
            err = { 'error': 'Invalid Parameters'}
            return render(request, 'users/registration.html', err )

    context = {}
    return render(request, 'users/registration.html', context)

def logout_request(request):
    logout(request)
    return HttpResponseRedirect(reverse('base:logged_out'))