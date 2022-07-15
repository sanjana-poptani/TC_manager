from audioop import reverse
from curses.ascii import US
from enum import unique
from http.client import HTTPResponse
import imp
from os import uname
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render,HttpResponse
from django.contrib import messages
from django.contrib.auth.hashers import make_password,check_password
from .models import *

# Create your views here.
def home(request):
    return render(request,"home.html")



def login(request):
    return render(request,"login.html")


def signup(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        usrname = request.POST.get('uname')
        pwd = request.POST.get('pwd')
        cpwd = request.POST.get('cpwd')


        # pwd and confirm pwd must be same
        if pwd != cpwd: 
            # return render(request,"signup.html",{'message':'Password and confirm password must be same!'})
            messages.error(request,"Password and confirm password must be same!")
            return HttpResponseRedirect("signup")
        

        # email must be unique
        if User.objects.filter(uname = usrname).first():
            messages.error('Username is already taken! Please try with another username')
        if User.objects.filter(uname = usrname).first():
            messages.error('Username is already taken! Please try with another username')


        pwdd = make_password(pwd)

        if email.endswith("@kristal.ai") == False:
            messages.error(request,"Please register with your Kristal's id!")
            return HttpResponseRedirect("signup")

        user_obj = User.objects.create(uname = usrname,email = email,pwd = pwdd)
        user_obj.save()

        messages.success(request,"Registration successful!")
        return redirect('/')

    else:

        return render(request,"signup.html")


def cards(request):
    return render(request,"cards.html")

def releases(request):
    return render(request,"releases.html")

def release_sheet(request):
    return render(request,"release_sheet.html")