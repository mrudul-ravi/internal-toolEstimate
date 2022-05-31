from __future__ import unicode_literals
from django.db import models
import datetime
from django.contrib.auth.models import User

# Create your models here.
import logging
from django.utils import timezone

from django.urls import reverse

from django.core.mail import send_mail
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser

from django.contrib.auth.models import AbstractUser


class Invoice1(models.Model):
    customer = models.CharField(max_length=100)
    bill_titlefront = models.CharField(max_length=100)
    bill_titleback = models.CharField(max_length=100)
    bill_title = models.CharField(max_length=100)
    termsandconditions = models.CharField(max_length=100)
    fulldescription = models.CharField(max_length=100)
    date = models.DateField()
    service_type = models.CharField(max_length=100)
    total_amount = models.DecimalField(max_digits=100, decimal_places=2, blank=True, null=True)
    service = models.TextField(max_length=100)
    gst = models.CharField(max_length=100)
    gsttotal = models.CharField(max_length=100)
    subtotal = models.CharField(max_length=100)
    gstpercentage = models.CharField(max_length=100)
    status = models.BooleanField(default=False)
    currency = models.TextField(max_length=100)
    footer = models.TextField(max_length=100)

    def __str__(self):
        return str(self.customer)

    def get_status(self):
        return self.status

    # def save(self, *args, **kwargs):
    # if not self.id:
    #     self.due_date = datetime.datetime.now()+ datetime.timedelta(days=15)
    # return super(Invoice, self).save(*args, **kwargs)


class Invoice2(models.Model):
    customer = models.CharField(max_length=100)
    bill_title = models.CharField(max_length=100)
    termsandconditions = models.CharField(max_length=100)
    fulldescription = models.CharField(max_length=100)
    date = models.DateField()
    service_type = models.CharField(max_length=100)
    total_amount = models.DecimalField(max_digits=100, decimal_places=2, blank=True, null=True)
    service = models.TextField(max_length=100)
    subtotal = models.CharField(max_length=100)
    status = models.BooleanField(default=False)
    currency = models.TextField(max_length=100)
    footer = models.TextField(max_length=100)

    def __str__(self):
        return str(self.customer)

    def get_status(self):
        return self.status

    # def save(self, *args, **kwargs):
    # if not self.id:
    #     self.due_date = datetime.datetime.now()+ datetime.timedelta(days=15)
    # return super(Invoice, self).save(*args, **kwargs)


class LineItem1(models.Model):
    customer = models.ForeignKey(Invoice1, on_delete=models.CASCADE)
    service = models.TextField()
    description = models.TextField()
    quantity = models.IntegerField()
    rate = models.DecimalField(max_digits=100, decimal_places=2)
    amount = models.DecimalField(max_digits=100, decimal_places=2)

    def __str__(self):
        return str(self.customer)


class LineItem2(models.Model):
    customer = models.ForeignKey(Invoice2, on_delete=models.CASCADE)
    service = models.TextField()
    description = models.TextField()
    quantity = models.IntegerField()
    amount = models.CharField(max_length=100)

    def __str__(self):
        return str(self.customer)

class Customers(models.Model):
    name = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    contact1 = models.CharField(max_length=100)
    def __str__(self):
        return str(self.name)

