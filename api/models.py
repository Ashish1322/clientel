

from django.db import models

# Create your models here.





class Account(models.Model):
    id = models.CharField(max_length=100,primary_key=True)
    name = models.CharField(max_length=50,default="")
    def __str__(self):
        return self.name

class Userm(models.Model):
    id = models.CharField(max_length=100,primary_key=True)
    name = models.CharField(max_length=50,default="")
    def __str__(self):
        return self.name

class Opportunity(models.Model):
    id = models.CharField(max_length=100,primary_key=True)
    name = models.CharField(max_length=50,default="")
    amount = models.BigIntegerField(default=0)
    accountId = models.ForeignKey(Account, on_delete=models.CASCADE , null=True)
    userId = models.ForeignKey(Userm,on_delete=models.CASCADE , null=True)
    def __str__(self):
        return self.name
# abc
# 1234