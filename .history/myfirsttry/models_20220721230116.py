import email
from operator import mod
from pyexpat import model
from statistics import mode
from tkinter.tix import Tree
from unicodedata import name
from djongo import models

# Create your models here.
class User(models.Model):
    id = models.AutoField(primary_key=True)
    # name = models.CharField(max_length=255)
    uname = models.CharField(max_length=255)
    email = models.EmailField()
    pwd = models.CharField(max_length=255)
    is_verified = models.BooleanField(default=False)
    otp = models.IntegerField()


class Card(models.Model):
    id = models.AutoField(primary_key=True)
    release_num = models.IntegerField()
    release_num_word = models.CharField(max_length=50)
    release_desc = models.TextField()


class Scope(mo)