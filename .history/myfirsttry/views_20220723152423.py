from audioop import reverse
from curses.ascii import US
from enum import unique
from http.client import HTTPResponse
import imp
from num2words import num2words
# from os import uname
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render,HttpResponse
from django.contrib import messages
from django.contrib.auth.hashers import make_password,check_password
from .models import *
from django.contrib.sessions.models import Session
Session.objects.all().delete()
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
    if 'email' in request.session and 'id' in request.session:
        card_details = Release.objects.all()
        return render(request,"cards.html",{'cards':card_details})
    else:
        return redirect("/")

def release_scope(request,id):
    if 'email' in request.session and 'id' in request.session:
        release = Release.objects.get(id = id)
        # to check if scope exist
        try:
            print("--------------I reached in try::)) ---------" + str(release.id) + "--------------- and -------------" + str(release))
            release_scopes = Scope.objects.get(release_id = release)
            print("---------------oh yeeahhh, i got scope------------------" + release_scope.id)
            return render(request,"release_scope.html",{'scopes':release_scopes})
        except:
            print("-----------------I reached here:)")
            
            print("-----------------------I got a release card!!!!---------------" + str(release.id))
            return render(request,"release_scope.html",{'release' : release})
    else:
        return redirect("/")

def release_sheet(request):
    if not 'email' in request.session:
        return redirect("/")
    return render(request,"release_sheet.html")

def card_add(request):
    if 'email' in request.session and 'id' in request.session:
        if request.method == "POST":
            rnum = request.POST.get('rversion')
            desc = request.POST.get('rdesc')

            word = num2words(rnum,to = 'ordinal')

            card_obj = Release.objects.create(release_num = rnum,release_num_word = word,release_desc = desc)
            card_obj.save()

        return redirect('/cards')
    else:
        return redirect('/')


def scope_add(request,id):
    if 'email' in request.session and 'id' in request.session:
        if request.method == "POST":
            epic = request.POST.get('epic')
            edesc = request.POST.get('edesc')
            release_id = Release.objects.get(id = id)

            user = User.objects.get(id = request.session['id'])

            scope_obj = Scope.objects.create(epic = epic,scope_desc = edesc,release_id = release_id,user_id = user)
            scope_obj.save()

        return redirect('/release_scope/' + str(id))
    else:
        return redirect('/')

def del_card(request,id):
    if 'email' in request.session and 'id' in request.session:
        obj = Release.objects.get(id = id)
        obj.delete()
        return redirect ('/cards')
    else:
        return redirect('/')

def edit_card(request,id):
    if 'email' in request.session and 'id' in request.session:
        obj = Release.objects.get(id = id)
        if request.method == "POST":
            rnum = request.POST.get("rversion")
            rdesc = request.POST.get("rdesc")

            wordd = num2words(rnum,to = 'ordinal')
            obj.release_num = rnum
            obj.release_num_word = wordd
            obj.release_desc = rdesc

            obj.save()
            return redirect('/cards')

        else:
            return render(request,"cards.html",{'objj':obj})
            
    else:
        return redirect('/')

def logout(request):
    if 'email' in request.session and 'id' in request.session:
        del request.session['email']
        del request.session['uname']
        del request.session['id']
        return redirect('/')