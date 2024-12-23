from django.shortcuts import render,redirect
from django.contrib.auth.models import User,auth
from .models import *
from django.core.mail import send_mail
from django.conf import settings
from django.core.mail import EmailMultiAlternatives

# Create your views here.
def register(request):
    if request.method == 'POST':
        firstname=request.POST['firstname']
        lastname=request.POST['lastname']
        username=request.POST['username']
        email=request.POST['email']
        password=request.POST['password']
        confirm_password=request.POST['confirm_password']
        error={}
        if User.objects.filter(username=username).exists():
            error['username']='username is already exists'
        if (password!=confirm_password):
            error['password']='password is not matching'
        if error:
             return render(request,'register.html',{'error':error})
        user=User.objects.create_user(username=username,first_name=firstname,last_name=lastname,email=email,password=password)
        user.save()
        acc=account(username=username,first_name=firstname,last_name=lastname,account_balance=0,email=email)
        acc.save()
        with open('template/account_creation_success.html','r')as file:
            html_content=file.read()
            html_content=html_content.replace('{firstname}',firstname)
        subject='Account Created Successfully'
        from_email=settings.EMAIL_HOST_USER
        recipient_list=[email]
        email_account_creation=EmailMultiAlternatives(subject,'',from_email,recipient_list)
        email_account_creation.attach_alternative(html_content,'text/html')
        email_account_creation.send()
        return redirect('/regsuccess/')
    return render(request, 'register.html')


def login(request):
    if request.method == 'POST':
        username=request.POST['username']
        password=request.POST['password']
        user=auth.authenticate(username=username,password=password)
        error={}
        if user is None:
            error['username']='username not found'
            return render(request,'login.html',{'error':error})
        auth.login(request,user)
        return redirect('/loginsuccess/')
    return render(request, 'login.html')


def homepage(request):
    return render(request,'homepage.html')

def logout(request):
    auth.logout(request)
    return redirect('/')

def lobby(request):
    if request.user.is_authenticated:
        return render(request,'lobby.html')
    else:
        return redirect('/login/')
    
def deposite(request):
    Account=account.objects.get(username=request.user.username)
    if request.method=='POST':
        amount=request.POST['amount']
        Account.account_balance+=int(amount)
        Account.save()
        trans=transaction(transaction_type='deposite',
                      main_username=request.user.username,
                      sender_username='system',
                      amount_deducted=amount,
                      receiver_name=request.user.username,
                      amount_received=amount,
                      balance=Account.account_balance,)
        trans.save()
        with open('template/account_deposite_success.html','r')as file:
            html_content=file.read()
            html_content=html_content.replace('{firstname}',request.user.username)
        subject='Account Created Successfully'
        from_email=settings.EMAIL_HOST_USER
        recipient_list=[Account.email]
        email_account_creation=EmailMultiAlternatives(subject,'',from_email,recipient_list)
        email_account_creation.attach_alternative(html_content,'text/html')
        email_account_creation.send()
        return redirect('/depositesuccess/')
    return render(request,'deposite.html')

def withdraw(request):
    Account=account.objects.get(username=request.user.username)
    if request.method=='POST':
        amount=request.POST['amount']
        Account.account_balance-=int(amount)
        Account.save()
        trans=transaction(transaction_type='withdraw',
                      main_username=request.user.username,
                      sender_username=request.user.username,
                      amount_deducted=amount,
                      receiver_name='system',
                      amount_received=amount,
                      balance=Account.account_balance,)
        trans.save()
        with open('template/account_withdraw_success.html','r')as file:
            html_content=file.read()
            html_content=html_content.replace('{firstname}',request.user.username)
        subject='Account Created Successfully'
        from_email=settings.EMAIL_HOST_USER
        recipient_list=[Account.email]
        email_account_creation=EmailMultiAlternatives(subject,'',from_email,recipient_list)
        email_account_creation.attach_alternative(html_content,'text/html')
        email_account_creation.send()
        return redirect('/withdrawsuccess/')
    return render(request,'withdraw.html')

def sendmoney(request):
    non_staff_users=User.objects.filter(is_staff=False).exclude(username=request.user.username)
    if request.method=='POST':
        recipient_username=request.POST['recipient']
        amount=request.POST['amount']
        sender=account.objects.get(username=request.user.username)
        recipient=account.objects.get(username=recipient_username)
        if int(amount)<=sender.account_balance:
            sender.account_balance-=int(amount)
            sender.save()
            recipient.account_balance+=int(amount)
            recipient.save()
            trans=transaction(transaction_type='sendmoney',
                      main_username=sender.username,
                      sender_username=sender.username,
                      amount_deducted=amount,
                      receiver_name=recipient.username,
                      amount_received=amount,
                      balance=sender.account_balance,)
            trans.save()
            with open('template/account_sendmoney_success.html','r')as file:
                html_content=file.read()
                html_content=html_content.replace('{firstname}',request.user.username)
            subject='Account Created Successfully'
            from_email=settings.EMAIL_HOST_USER
            recipient_list=[sender.email]
            email_account_creation=EmailMultiAlternatives(subject,'',from_email,recipient_list)
            email_account_creation.attach_alternative(html_content,'text/html')
            email_account_creation.send()
            trans=transaction(transaction_type='sendmoney',
                      main_username=recipient.username,
                      sender_username=sender.username,
                      amount_deducted=amount,
                      receiver_name=recipient.username,
                      amount_received=amount,
                      balance=recipient.account_balance,)
            trans.save()
            with open('template/account_deposite_success.html','r')as file:
                html_content=file.read()
                html_content=html_content.replace('{firstname}',request.user.username)
            subject='Account Created Successfully'
            from_email=settings.EMAIL_HOST_USER
            recipient_list=[recipient.email]
            email_account_creation=EmailMultiAlternatives(subject,'',from_email,recipient_list)
            email_account_creation.attach_alternative(html_content,'text/html')
            email_account_creation.send()
            return redirect('/sendmoneysuccess/')
        else:
            error={}
            error['error']='Insufficient balance'
            return render(request,'sendmoney.html',{'error':error})
    return render(request,'sendmoney.html',{'non_staff_users':non_staff_users})

def transcation(request):
    trans=transaction.objects.filter(main_username=request.user.username)
    return render(request,'transaction.html',{'trans':trans})
    
def regsuccess(request):
    return render(request,'regsuccess.html')

def loginsuccess(request):
    return render(request,'loginsuccess.html')

def depositesuccess(request):
    return render(request,'depositesuccess.html')

def withdrawsuccess(request):
    return render(request,'withdrawsuccess.html')

def sendmoneysuccess(request):
    return render(request,'sendmoneysuccess.html')









