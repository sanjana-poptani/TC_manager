from audioop import reverse
from cgi import test
from curses.ascii import US
from enum import unique
from http.client import HTTPResponse
import imp
from tkinter.messagebox import NO
from urllib import request
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
        return redirect('/verify')

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
            release_scopes = Scope.objects.filter(release_id = release)
            print("-------------------I got scope--------------------- " + str(release_scopes))
            for release_scopee in release_scopes:
                print("---------------oh yeeahhh, i got scope------------------" + str(release_scopee.id))
            return render(request,"release_scope.html",{'scopes':release_scopes,'release':release})
        except Exception as e:
            print("-----------------I reached here becozz---------------- " + str(e))
            return render(request,"release_scope.html",{'release' : release})
    return redirect("/")

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

        return HttpResponseRedirect('/release_scope/' + str(id))
    else:
        return redirect('/')

def del_card(request,id):
    if 'email' in request.session and 'id' in request.session:
        obj = Release.objects.get(id = id)
        obj.delete()
        return redirect ('/cards')
    else:
        return redirect('/')


def del_scope(request,id):
    if 'email' in request.session and 'id' in request.session:
        obj = Scope.objects.get(id = id)
        card_id = obj.release_id
        obj.delete()
        return HttpResponseRedirect('/release_scope/' + str(card_id.id))
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


def edit_scope(request,id,rid):
    if 'email' in request.session and 'id' in request.session:
        obj = Scope.objects.get(id = id)
        release = Release.objects.get(id = rid)
        if request.method == 'POST':
            epic = request.POST.get('epic')
            edesc = request.POST.get('desc')


            obj.epic = epic
            obj.scope_desc = edesc
            obj.release_id = release
            obj.save()
            return HttpResponseRedirect('/release_scope/' + str(rid))

        else:
            all_obj = Scope.objects.all()
            print("Yeaah reached here----------")
            return render(request,"release_scope.html",{'scopes':all_obj,'edit_obj':obj,'release':release})

    else:
        return redirect('/')


def edit_TC(request,id,tid):
    if 'email' in request.session and 'id' in request.session:
        scope = Scope.objects.get(id = id)
        print("------------------scope-----------------")
        print(scope)
        obj = TestCase.objects.filter(scope_id = scope)
        print(obj)
        testcase = TestCase.objects.get(id = tid)

        if request.method == 'POST':
            ucase = request.POST.get('usecase')
            steps = request.POST.get('steps')
            eresult = request.POST.get('expected')
            ts_portal = request.POST.get('ts_portal')
            tester_portal = request.POST.get('tester_portal')
            ts_rm = request.POST.get('ts_rm')
            tester_rm = request.POST.get('tester_rm')
            ts_internal = request.POST.get('ts_internal')
            tester_internal = request.POST.get('tester_internal')
            ts_be = request.POST.get('ts_be')
            tester_be = request.POST.get('tester_internal')
            ts_ios = request.POST.get('ts_ios')
            tester_ios = request.POST.get('tester_ios')
            ts_android = request.POST.get('ts_android')
            tester_android = request.POST.get('tester_android')
            ts_automation = request.POST.get('ts_automation')
            tester_automation = request.POST.get('tester_automation')
            tester_comment = request.POST.get('tcmnt')
            reviewer_comment = request.POST.get('rcmnt')
            tc_author = request.POST.get('tc_author')

            if tester_portal == "NA":
                tester_portal = None
            else:
                tester_portal = User.objects.get(uname = tester_portal)

                
            if tester_rm == "NA":
                print("---------------- reached here -------------")
                tester_rm = None
            else:
                print("------------------ in else------------------- "+ tester_rm)
                tester_rm = User.objects.get(uname = tester_rm)

                
            if tester_internal == "NA":
                print("---------------came in if--------" + str(tester_internal))
                tester_internal = None
            else:
                print("---------got tester " + str(tester_internal))
                tester_internal = User.objects.get(uname = tester_internal)

                
            if tester_be == "NA":
                tester_be = None
            else:
                tester_be = User.objects.get(uname = tester_be)

                
            if tester_ios == "NA":
                tester_ios = None
            else:
                tester_ios = User.objects.get(uname = tester_ios)

                
            if tester_android == "NA":
                tester_android = None
            else:
                tester_android = User.objects.get(uname = tester_android)

                
            if tester_automation == "NA":
                tester_automation = None
            else:
                tester_automation = User.objects.get(uname = tester_automation)

            if tc_author == "NA":
                tc_author = None
            else:
                tc_author = User.objects.get(uname = tc_author)


            testcase.usecase = ucase
            testcase.steps = steps
            testcase.expected_result = eresult
            testcase.ts_portal = ts_portal
            testcase.ts_rm = ts_rm
            testcase.ts_internal = ts_internal
            testcase.ts_be = ts_be
            testcase.ts_ios = ts_ios
            testcase.ts_android = ts_android
            testcase.ts_automation = ts_automation
            testcase.tester_portal = tester_portal
            testcase.tester_rm = tester_rm
            testcase.tester_internal = tester_internal
            testcase.tester_be = tester_be
            testcase.tester_ios = tester_ios
            testcase.tester_android = tester_android
            testcase.tester_automation = tester_automation
            testcase.tester_comment = tester_comment
            testcase.reviewer_comment = reviewer_comment
            testcase.tc_author = tc_author
            testcase.scope_id = scope

            testcase.save()

            return redirect("/view_tcs/" + str(id))

        else:
            users = User.objects.all()
            return render(request,"release_sheet.html",{'tcs':obj,'users':users,'scope':scope,'editobj':testcase})


def filter_TC(request,id):
    if 'email' in request.session and 'id' in request.session:
        scope = Scope.objects.get(id = id)
        objs = TestCase.objects.filter(scope_id = scope)

        if request.method == 'POST':
            test_status = request.POST.get("testcase")
            tester = request.POST.get("tester")
            portal = False
            rm = False
            internal = False
            be = False
            ios = False
            android = False
            automation = False

            for obj in objs:
                if obj.ts_portal == test_status and obj.tester_portal == tester:
                    portal = True

                if obj.ts_rm == test_status and obj.tester_rm == tester:
                    rm = True

                if obj.ts_internal == test_status and obj.tester_internal == tester:
                    internal = True

                if obj.ts_be == test_status and obj.tester_be == tester:
                    be = True

                if obj.ts_ios == test_status and obj.tester_ios == tester:
                    ios = True

                if obj.ts_android == test_status and obj.tester_android == tester:
                    android = True

                if obj.ts_automation == test_status and obj.tester_automation == tester:
                    automation = True

        

def view_TCs(request,id):
    if 'email' in request.session and 'id' in request.session:
        scope = Scope.objects.get(id = id)
        obj = TestCase.objects.filter(scope_id = scope)
        print("-------------------Reached here-------------- and got------------" + str(obj))
        users = User.objects.all()
        return render(request,"release_sheet.html",{'tcs':obj,'users':users,'scope':scope})
    else:
        return redirect('/')


def add_TC(request,id):
    if 'email' in request.session and 'id' in request.session:
        scope = Scope.objects.get(id = id)
        obj = TestCase.objects.filter(scope_id = scope)
        users = User.objects.all()
        if request.method == 'GET':
            return render(request,"release_sheet.html",{'tcs':obj,'users':users,'scope':scope,'add':True})

        else:
            ucase = request.POST.get('usecase')
            steps = request.POST.get('steps')
            eresult = request.POST.get('expected')
            ts_portal = request.POST.get('ts_portal')
            tester_portal = request.POST.get('tester_portal')
            ts_rm = request.POST.get('ts_rm')
            tester_rm = request.POST.get('tester_rm')
            ts_internal = request.POST.get('ts_internal')
            tester_internal = request.POST.get('tester_internal')
            ts_be = request.POST.get('ts_be')
            tester_be = request.POST.get('tester_internal')
            ts_ios = request.POST.get('ts_ios')
            tester_ios = request.POST.get('tester_ios')
            ts_android = request.POST.get('ts_android')
            tester_android = request.POST.get('tester_android')
            ts_automation = request.POST.get('ts_automation')
            tester_automation = request.POST.get('tester_automation')
            tester_comment = request.POST.get('tcmnt')
            reviewer_comment = request.POST.get('rcmnt')
            tc_author = request.POST.get('tc_author')

            if tester_portal == "NA":
                tester_portal = None
            else:
                tester_portal = User.objects.get(uname = tester_portal)

                
            if tester_rm == "NA":
                print("---------------- reached here -------------")
                tester_rm = None
            else:
                print("------------------ in else------------------- "+ tester_rm)
                tester_rm = User.objects.get(uname = tester_rm)

                
            if tester_internal == "NA":
                print("---------------came in if--------" + str(tester_internal))
                tester_internal = None
            else:
                print("---------got tester " + str(tester_internal))
                tester_internal = User.objects.get(uname = tester_internal)

                
            if tester_be == "NA":
                tester_be = None
            else:
                tester_be = User.objects.get(uname = tester_be)

                
            if tester_ios == "NA":
                tester_ios = None
            else:
                tester_ios = User.objects.get(uname = tester_ios)

                
            if tester_android == "NA":
                tester_android = None
            else:
                tester_android = User.objects.get(uname = tester_android)

                
            if tester_automation == "NA":
                tester_automation = None
            else:
                tester_automation = User.objects.get(uname = tester_automation)

            if tc_author == "NA":
                tc_author = None
            else:
                tc_author = User.objects.get(uname = tc_author)

            new_obj = TestCase.objects.create(usecase = ucase,steps = steps,expected_result = eresult,
            ts_portal = ts_portal,ts_rm = ts_rm,ts_internal = ts_internal,
            ts_be = ts_be,ts_ios = ts_ios,ts_android = ts_android,
            ts_automation = ts_automation,
            tester_portal = tester_portal,
            tester_rm = tester_rm,
            tester_internal = tester_internal,
            tester_be = tester_be,
            tester_ios = tester_ios,
            tester_android = tester_android,
            tester_automation = tester_automation,
            tester_comment = tester_comment,
            reviewer_comment = reviewer_comment,
            tc_author = tc_author,
            scope_id = scope
            )

            new_obj.save()

            return redirect("/view_tcs/" + str(id))

    else:
        return redirect("/")


def del_TCs(request,id):
    if 'email' in request.session and 'id' in request.session:
        TC = TestCase.objects.get(id = id)
        scope = TC.scope_id
        TC.delete()
        return HttpResponseRedirect("/view_tcs/" + str(scope.id))

def logout(request):
    if 'email' in request.session and 'id' in request.session:
        del request.session['email']
        del request.session['uname']
        del request.session['id']
        return redirect('/')