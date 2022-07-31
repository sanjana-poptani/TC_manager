from audioop import reverse
from cgi import test
from curses.ascii import US
from enum import auto, unique
from http.client import HTTPResponse
import imp
import io
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
            print("-----------------------------------" + str(card_obj.id) + " " + str(card_obj.release_num))
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
        print("----------------- I reached in edit_TC----------------------")
        scope = Scope.objects.get(id = id)
        print("------------------scope-----------------")
        print(scope)
        title = TestCase_Title.objects.get(scope_id = scope)
        print(title)
        testcase = TestCase.objects.filter(title_id = title)
        tc = TestCase.objects.get(id = tid,title_id = title)
        print("-------Got TC ---------------" + str(tc))

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
            comment = request.POST.get('tcmnt')

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


            tc.usecase = ucase
            tc.steps = steps
            tc.expected_result = eresult
            tc.ts_portal = ts_portal
            tc.ts_rm = ts_rm
            tc.ts_internal = ts_internal
            tc.ts_be = ts_be
            tc.ts_ios = ts_ios
            tc.ts_android = ts_android
            tc.ts_automation = ts_automation
            tc.tester_portal = tester_portal
            tc.tester_rm = tester_rm
            tc.tester_internal = tester_internal
            tc.tester_be = tester_be
            tc.tester_ios = tester_ios
            tc.tester_android = tester_android
            tc.tester_automation = tester_automation
            tc.comment = comment
            tc.title_id = title
            tc.save()

            return redirect("/view_tcs/" + str(id))

        else:
            users = User.objects.all()
            return render(request,"release_sheet.html",{'tcs':testcase,'users':users,'scope':scope,'editobj':tc})


def filter_TC(request,id):
    if 'email' in request.session and 'id' in request.session:
        scope = Scope.objects.get(id = id)
        title = TestCase_Title.objects.get(scope_id = scope)
        objs = TestCase.objects.filter(title_id = title)
        print("---------------------------------------")
        print(objs)
        users = User.objects.all()

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

            # print("----------------yayy reached in filter, objs -----------" + str(objs))

            for obj in objs:
                print("---------------" + str(obj.tester_internal))
                if obj.ts_portal == test_status and obj.tester_portal != None and obj.tester_portal.uname == tester:
                    portal = True

                if obj.ts_rm == test_status and obj.tester_rm != None and obj.tester_rm.uname == tester:
                    rm = True

                if obj.ts_internal == test_status and obj.tester_internal != None and obj.tester_internal.uname == tester:
                    internal = True

                if obj.ts_be == test_status and obj.tester_be != None and obj.tester_be.uname == tester:
                    be = True

                if obj.ts_ios == test_status and obj.tester_ios != None and obj.tester_ios.uname == tester:
                    ios = True

                if obj.ts_android == test_status and obj.tester_android != None and obj.tester_android.uname == tester:
                    android = True

                if obj.ts_automation == test_status and obj.tester_automation != None and obj.tester_automation.uname == tester:
                    automation = True

            return render(request,"release_sheet.html",{'tcs':objs,
            'users':users,
            'scope':scope,
            'filter':True,
            'portal':portal,
            'rm':rm,
            'internal':internal,
            'be':be,
            'ios':ios,
            'android':android,
            'automation':automation})

    else:
        return redirect('/')

def view_TCs(request,id):
    if 'email' in request.session and 'id' in request.session:
        users = User.objects.all()
        scope = Scope.objects.get(id = id)

        try:
            title = TestCase_Title.objects.get(scope_id = scope)
            obj = TestCase.objects.filter(title_id = title)
            print("-------------------Reached here-------------- and got------------")
            for o in obj:
                print("" " + str(o.tester_portal) + " " str(o.tester_rm) + " " str(o.tester_internal) + " " str(o.tester_be) + " " str(o.tester_ios) + " " str(o.tester_android) + " " str(o.tester_automation) + " ")
            return render(request,"release_sheet.html",{'title':title,'tcs':obj,'users':users,'scope':scope})

        except Exception as e:
            print("--------------Reached in except--------------becox-------------" + str(e) )
            return render(request,"release_sheet.html",{'users':users,'scope':scope})


    else:
        return redirect('/')


def add_TC(request,id):
    if 'email' in request.session and 'id' in request.session:
        scope = Scope.objects.get(id = id)
        users = User.objects.all()
        
        
        if request.method == 'GET':
            print("------------Reached in if ")
            try:
                print("-----------------Reached in try----------------------")
                title = TestCase_Title.objects.get(scope_id = scope)
                obj = TestCase.objects.filter(title_id = title)
                return render(request,"release_sheet.html",{'tcs':obj,'users':users,'scope':scope,'add':True})

            except:
                return render(request,"release_sheet.html",{'scope':scope,'add':True})

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
            comment = request.POST.get('tcmnt')

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



            try: 
                title = TestCase_Title.objects.get(scope_id = scope)
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
                comment = comment,
                title_id = title
                )
                new_obj.save()

            except:
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
                comment = comment,
                )

                new_obj.save()

            return redirect("/view_tcs/" + str(id))

    else:
        return redirect("/")


def add_details(request,id):
    if 'email' in request.session and 'id' in request.session:
        scope = Scope.objects.get(id = id)
        users = User.objects.all()

        if request.method == "POST":
            title = request.POST.get('title')
            tc_author = request.POST.get('author')

            new_TC = TestCase_Title.objects.create(tc_author = tc_author,scope_id = scope,title = title)
            new_TC.save()
            return redirect("/view_tcs/" + str(id))

        else:
            try:
                title = TestCase_Title.objects.get(scope_id = id)
                tc = TestCase.objects.filter(title_id = title)
                return render(request,"release_sheet.html",{'tcs':tc,'users':users,'scope':scope,'add_title':True})

            except:
                return render(request,"release_sheet.html",{'users':users,'scope':scope,'add_title':True})

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