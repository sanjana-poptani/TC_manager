import email
from unicodedata import name
from djongo import models

# Create your models here.
class User(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    uname = models.CharField(max_length=255)
    email = models.EmailField()
    pwd = models.CharField(max_length=255)