import email
from operator import mod
from pyexpat import model
from statistics import mode
from tkinter import CASCADE
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


class Release(models.Model):
    id = models.AutoField(primary_key=True)
    release_num = models.IntegerField()
    release_num_word = models.CharField(max_length=50)
    release_desc = models.TextField()


class Scope(models.Model):
    id = models.AutoField(primary_key=True)
    epic = models.CharField(max_length=255)
    scope_desc = models.TextField()
    release_id = models.ForeignKey(Release,on_delete=models.CASCADE)
    user_id = models.ForeignKey(User,on_delete=models.CASCADE)



class TestCase(models.Model):
    id = models.AutoField(primary_key=True)
    usecase = models.CharField(max_length=200)
    steps = models.TextField()
    expected_result = models.TextField()
    ts_portal = models.CharField(max_length=15)
    ts_rm = models.CharField(max_length=15)
    ts_internal = models.CharField(max_length=15)
    ts_be = models.CharField(max_length=15)
    ts_ios = models.CharField(max_length=15)
    ts_android = models.CharField(max_length=15)
    ts_automation = models.ForeignKey(User,max_length=15)
    tester_portal = models.CharField(max_length=15)
    tester_rm = models.CharField(max_length=15)
    tester_internal = models.CharField(max_length=15)
    tester_be = models.CharField(max_length=15)
    tester_ios = models.CharField(max_length=15)
    tester_android = models.CharField(max_length=15)
    tester_automation = models.CharField(max_length=15)
    tester_comment = models.TextField()
    reviewer_comment = models.TextField()
    tc_author = models.CharField(max_length=15)