from django.urls import path
from .views import *

app_name='mybank'

urlpatterns=[
    path('login/',login,name='login'),
    path('register/',register,name='register'),
    path('',homepage,name='homepage'),
    path('lobby/',lobby,name='lobby'),
    path('logout/',logout,name='logout'),
    path('deposite/',deposite,name='deposite'),
    path('withdraw/',withdraw,name='withdraw'),
    path('sendmoney/',sendmoney,name='sendmoney'),
    path('transcation/',transcation,name='transcation'),
    path('regsuccess/',regsuccess,name='regsuccess'),
    path('loginsuccess/',loginsuccess,name='loginsuccess'),
    path('depositesuccess/',depositesuccess,name='depositesuccess'),
    path('withdrawsuccess/',withdrawsuccess,name='withdrawsuccess'),
    path('sendmoneysuccess/',sendmoneysuccess,name='sendmoneysuccess'),
]
