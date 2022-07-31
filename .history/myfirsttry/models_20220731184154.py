import email
from operator import mod
from pyexpat import model
from re import T
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



class TestCase_Title(models.Model):
    title_id = models.AutoField(primary_key=True)
    tc_author = models.CharField(max_length=500)
    scope_id = models.ForeignKey(Scope,on_delete = models.CASCADE)
    title = models.CharField(max_length=255)


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
    ts_automation = models.CharField(max_length=15)
    tester_portal = models.ForeignKey(User,on_delete=models.CASCADE,related_name='tester_portal',blank=True,null=True)
    tester_rm = models.ForeignKey(User,on_delete=models.CASCADE,related_name='tester_rm',blank=True,null=True)
    tester_internal = models.ForeignKey(User,on_delete=models.CASCADE,related_name='tester_internal',blank=True,null=True)
    tester_be = models.ForeignKey(User,on_delete=models.CASCADE,related_name='tester_be',blank=True,null=True)
    tester_ios = models.ForeignKey(User,on_delete=models.CASCADE,related_name='tester_ios',blank=True,null=True)
    tester_android = models.ForeignKey(User,on_delete=models.CASCADE,related_name='tester_android',blank=True,null=True)
    tester_automation = models.ForeignKey(User,on_delete=models.CASCADE,related_name='tester_automation')
    comment = models.TextField()
    title_id = models.ForeignKey(TestCase_Title,on_delete=models.CASCADE)

