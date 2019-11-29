from django.db import models


class Customer(models.Model):
    name = models.CharField(max_length = 250)
    path = models.CharField(max_length=250)
