# Generated by Django 5.1.2 on 2024-12-22 16:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mybank', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='transaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('transaction_type', models.CharField(max_length=50)),
                ('main_username', models.CharField(max_length=50)),
                ('sender_username', models.CharField(max_length=50)),
                ('amount_deducted', models.IntegerField()),
                ('time_of_transaction', models.DateTimeField(auto_now_add=True)),
                ('receiver_name', models.CharField(max_length=50)),
                ('amount_received', models.IntegerField()),
                ('balance', models.IntegerField()),
            ],
        ),
    ]
