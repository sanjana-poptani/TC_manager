from audioop import reverse
from curses.ascii import US
from enum import unique
from http.client import HTTPResponse
import imp
from pydoc import render_doc
# from os import uname
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render,HttpResponse
from django.contrib import messages
from django.contrib.auth.hashers import make_password,check_password
from .models import *
from django.contrib.sessions.models import Session
from django.core.mail import send_mail
import math, random

# Create your views here.
def home(request):
    return render(request,"home.html")



def login(request):
    if request.method == "POST":
        # print("--------------------- reached in login ----------------")
        usrname = request.POST.get("uname")
        pwdd = request.POST.get("pwd")
        # pwd = make_password(pwdd)

        user = User.objects.get(uname = usrname)
        print("User found ----------- " + user.uname)


        # check user
        if not user.is_verified:
            messages.error(request,"Your email is not verified, pls check your email!!")
            return redirect("/verify")

        # print(pwd + " " + user.pwd)
        # check pwd
        if not check_password(pwdd,user.pwd):
            messages.error(request,"Password is invalid!! Pls try again!!")
            return redirect("/login")

        request.session['email'] = user.email
        request.session['uname'] = user.uname
        request.session['id'] = user.id
        print("--------------- session created ----------------")
        return redirect("/cards")

    else:
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


        user_obj = User.objects.create(uname = usrname,email = email,pwd = pwdd,otp = otp)
        user_obj.save()

        messages.success(request,"Otp sent to your mail!")
        return redirect('/')

    else:
        return render(request,"signup.html")


def verify(request):
    if request.method == "POST":
        ottp = request.POST.get("otp")

        usr = User.objects.filter(otp = ottp).first()

        if usr:

            if usr.is_verified:
                messages.info(request,"Already verified, pls try to login!!")
                return redirect("/login")

            messages.success(request,"OTP verified successfully!!")
            usr.is_verified = True
            usr.save()
            return redirect("/login")
        else:
            messages.error(request,"You entered wrong OTP!! Pls try again!!")
            return redirect("/verify")

    else:
        return render(request,"verify.html")

def generateOTP():
    digits = "0123456789"
    OTP = ""
    for i in range(4) :
        OTP += digits[math.floor(random.random() * 10)]
    return OTP

def cards(request):
    if not 'email' in request.session:
        return redirect("/")
    return render(request,"cards.html")

def releases(request):
    if not 'email' in request.session:
        return redirect("/")
    return render(request,"releases.html")

def release_sheet(request):
    if not 'email' in request.session:
        return redirect("/")
    return render(request,"release_sheet.html")


def logout(request):
    if 'email' in request.session and 'id' in request.session:
        del request.session['email']
        del request.session['username']
        del request.session['id']
        return redirect('/')