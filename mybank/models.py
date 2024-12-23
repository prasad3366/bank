from django.db import models

# Create your models here.
class account(models.Model):
    first_name=models.CharField(max_length=50)
    last_name=models.CharField(max_length=50)
    username=models.CharField(max_length=50)
    email=models.EmailField(max_length=100)
    account_balance=models.IntegerField()

class transaction(models.Model):
    transaction_type=models.CharField(max_length=50)
    main_username=models.CharField(max_length=50)
    sender_username=models.CharField(max_length=50)
    amount_deducted=models.IntegerField()
    time_of_transaction=models.DateTimeField(auto_now_add=True)
    receiver_name=models.CharField(max_length=50)
    amount_received=models.IntegerField()
    balance=models.IntegerField()

