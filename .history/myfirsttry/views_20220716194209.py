from audioop import reverse
from curses.ascii import US
from enum import unique
from http.client import HTTPResponse
import imp
# from os import uname
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render,HttpResponse
from django.contrib import messages
from django.contrib.auth.hashers import make_password,check_password
from .models import *
from django.core.mail import send_mail
import math, random

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
        if User.objects.filter(email = email).first():
            messages.error(request,'Email is already taken! Please try with another username')

        # username must be unique
        if User.objects.filter(uname = usrname).first():
            messages.error(request,'Username is already taken! Please try with another username')


        pwdd = make_password(pwd)

        if email.endswith("@kristal.ai") == False:
            messages.error(request,"Please register with your Kristal's id!")
            return HttpResponseRedirect("signup")


        # send otp
        otp = generateOTP()
        htmlgen = '<p>Your OTP is <strong>' + otp + '</strong></p>'
        send_mail("OTP request",otp,'testprojects1117@gmail.com',[email],fail_silently=False,html_message = htmlgen)


        user_obj = User.objects.create(uname = usrname,email = email,pwd = pwdd,)
        user_obj.save()

        messages.success(request,"Otp sent to your mail!")
        return redirect('/')

    else:

        return render(request,"signup.html")


def generateOTP():
    digits = "0123456789"
    OTP = ""
    for i in range(4) :
        OTP += digits[math.floor(random.random() * 10)]
    return OTP

def cards(request):
    return render(request,"cards.html")

def releases(request):
    return render(request,"releases.html")

def release_sheet(request):
    return render(request,"release_sheet.html")