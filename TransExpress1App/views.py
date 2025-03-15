import json

import requests
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from TransExpress1App.credentials import MpesaAccessToken, LipanaMpesaPpassword
from TransExpress1App.models import *
from django.contrib import messages
from requests.auth import HTTPBasicAuth


# Create your views here.
def starter(request):
    return render(request, 'starter-page.html')

def index(request):
    return render(request, 'index.html')

def about(request):
    return render(request, 'about.html')

def services(request):
    return render(request, 'services.html')

def quote(request):
    if request.method == "POST":
        myquote = Quote(
            depature = request.POST['departure'],
            delivery = request.POST['delivery'],
            weight = request.POST['Weight'],
            dimension = request.POST['dimension'],
            name = request.POST['name'],
            email = request.POST['email'],
            phone = request.POST['phone'],
            message = request.POST['message'],
        )
        myquote.save()
        return redirect('/quote')

    else:
        return render(request, 'get-a-quote.html')


def price(request):
    return render(request, 'pricing.html')

def contacts(request):
  return render(request,'contact,html')

def details(request):
    return render(request,'service-details.html')

def editquote(request, id):
    Quotes = get_object_or_404(Quote, id=id)
    if request.method == "POST":
        Quotes.departure = request.POST.get('departure')
        Quotes.delivery = request.POST.get('delivery')
        Quotes.weight= request.POST.get('weight')
        Quotes.dimension = request.POST.get('dimension')
        Quotes.name = request.POST.get('name')
        Quotes.email = request.POST.get('email')
        Quotes.phone = request.POST.get('phone')
        Quotes.message = request.POST.get('message')

        Quotes.save()
        return redirect('/show')

    else:
        return render(request, 'edit.html', {'Quote': Quote})

def deletequote(request, id):
   deletequote= Quote.objects.get(id=id)
   deletequote.delete()
   return redirect('/show')


def showquote(request):
    all = Quote.objects.all()
    return render(request, 'show.html', {'Quote': all})



def register(request):
    """ Show the registration form """
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        # Check the password
        if password == confirm_password:
            try:
                user = User.objects.create_user(username=username, password=password)
                user.save()

                # Display a message
                messages.success(request, "Account created successfully")
                return redirect('/login')
            except:
                # Display a message if the above fails
                messages.error(request, "Username already exist")
        else:
            # Display a message saying passwords don't match
            messages.error(request, "Passwords do not match")

    return render(request, 'register.html')



def login_view(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)

        # Check if the user exists
        if user is not None:
            # login(request, user)
            login(request, user)
            messages.success(request, "You are now logged in!")
            return redirect('/home')
        else:
            messages.error(request, "Invalid login credentials")

    return render(request, 'login.html')

#mpesa API
def token(request):
    consumer_key = '77bgGpmlOxlgJu6oEXhEgUgnu0j2WYxA'
    consumer_secret = 'viM8ejHgtEmtPTHd'
    api_URL = 'https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials'

    r = requests.get(api_URL, auth=HTTPBasicAuth(
        consumer_key, consumer_secret))
    mpesa_access_token = json.loads(r.text)
    validated_mpesa_access_token = mpesa_access_token["access_token"]

    return render(request, 'token.html', {"token":validated_mpesa_access_token})

def pay(request):
   return render(request, 'pay.html')


def stk(request):
    if request.method == "POST":
        phone = request.POST['phone']
        amount = request.POST['amount']
        access_token = MpesaAccessToken.validated_mpesa_access_token
        api_url = "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest"
        headers = {"Authorization": "Bearer %s" % access_token}
        request_data = {
            "BusinessShortCode": LipanaMpesaPpassword.Business_short_code,
            "Password": LipanaMpesaPpassword.decode_password,
            "Timestamp": LipanaMpesaPpassword.lipa_time,
            "TransactionType": "CustomerPayBillOnline",
            "Amount": amount,
            "PartyA": phone,
            "PartyB": LipanaMpesaPpassword.Business_short_code,
            "PhoneNumber": phone,
            "CallBackURL": "https://sandbox.safaricom.co.ke/mpesa/",
            "AccountReference": "Apen Softwares",
            "TransactionDesc": "Web Development Charges"
        }
        response = requests.post(api_url, json=request_data, headers=headers)

        # Parse response
        response_data = response.json()
        transaction_id = response_data.get("CheckoutRequestID", "N/A")
        result_code = response_data.get("ResponseCode", "1")  # 0 is success, 1 is failure

        # Save transaction to database
        transaction = Transaction(
            phone_number=phone,
            amount=amount,
            transaction_id=transaction_id,
            status="Success" if result_code == "0" else "Failed"
        )
        transaction.save()

        return HttpResponse(
            f"Transaction ID: {transaction_id}, Status: {'Success' if result_code == '0' else 'Failed'}")


def transactions_list(request):
    transactions = Transaction.objects.all().order_by('-date')
    return render(request, 'transactions.html', {'transactions': transactions})
