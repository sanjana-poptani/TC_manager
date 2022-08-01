from audioop import reverse
from cgi import test
from collections import defaultdict
from curses.ascii import US
from enum import auto, unique
from http.client import HTTPResponse
from django.db.models import Count, Q
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
            comment = request.POST.get('rcmnt')

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
            return render(request,"release_sheet.html",{'tcs':testcase,'users':users,'scope':scope,'editobj':tc,'title':title})


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
                if obj.tester_portal is None:
                    pass
                elif obj.ts_portal == test_status and obj.tester_portal.uname == tester:
                    portal = True

                if obj.tester_rm is None:
                    pass
                elif obj.ts_rm == test_status and obj.tester_rm.uname == tester:
                    rm = True

                if obj.tester_internal is None:
                    pass
                elif obj.ts_internal == test_status and obj.tester_internal.uname == tester:
                    internal = True

                if obj.tester_be is None:
                    pass
                elif obj.ts_be == test_status and obj.tester_be.uname == tester:
                    be = True

                if obj.tester_ios is None:
                    pass
                elif obj.ts_ios == test_status and obj.tester_ios.uname == tester:
                    ios = True

                if obj.tester_android is None:
                    pass
                elif obj.ts_android == test_status and obj.tester_android.uname == tester:
                    android = True

                if obj.tester_automation is None:
                    pass
                elif obj.ts_automation == test_status and obj.tester_automation.uname == tester:
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
            'automation':automation,
            'tester':tester,
            'ts':test_status,
            'title':title})

    else:
        return redirect('/')


def show_chart_Tc(request,id):
    if 'email' in request.session and 'id' in request.session:
        users = User.objects.all()
        scope = Scope.objects.get(id = id)
        title = TestCase_Title.objects.get(scope_id = scope)

        objs = TestCase.objects.filter(title_id = title)
        # tcs = TestCase.objects.filter(title_id = title).values('ts_portal').annotate(
        # portal_pass_count=Count('ts_portal',filter=Q(ts_portal='Pass')),
        # portal_fail_count=Count('ts_portal',filter=Q(ts_portal='Fail')),
        # portal_skip_count=Count('ts_portal',filter=Q(ts_portal='QA Skip')),
        # portal_yts_count=Count('ts_portal',filter=Q(ts_portal='YTS')),
        # portal_inprogress_count=Count('ts_portal',filter=Q(ts_portal='In_progress'))
        # )

        mainlist = []
        dic_portal = defaultdict(int)
        dic_rm = defaultdict(int)
        dic_internal = defaultdict(int)
        dic_android = defaultdict(int)
        dic_ios = defaultdict(int)
        dic_backend = defaultdict(int)
        dic_automation = defaultdict(int)

        for obj in objs:
            if obj.ts_portal == 'Pass':
                dic_portal['pass_count'] += 1
            
            elif obj.ts_portal == 'Fail':
                dic_portal['fail_count'] += 1
                
            elif obj.ts_portal == 'YTS':
                dic_portal['yts_count'] += 1
                
            elif obj.ts_portal == 'In_progress':
                dic_portal['inprogress_count'] += 1
                
            elif obj.ts_portal == 'QA Skip':
                dic_portal['skip_count'] += 1
                
            elif obj.ts_portal == 'NA':
                dic_portal['na_count'] += 1



            
            if obj.ts_rm == 'Pass':
                dic_rm['pass_count'] += 1
            
            elif obj.ts_rm == 'Fail':
                dic_rm['fail_count'] += 1
                
            elif obj.ts_rm == 'YTS':
                dic_rm['yts_count'] += 1
                
            elif obj.ts_rm == 'In_progress':
                dic_rm['inprogress_count'] += 1
                
            elif obj.ts_rm == 'QA Skip':
                dic_rm['skip_count'] += 1
                
            elif obj.ts_rm == 'NA':
                dic_rm['na_count'] += 1


            
            if obj.ts_internal == 'Pass':
                dic_internal['pass_count'] += 1
            
            elif obj.ts_internal == 'Fail':
                dic_internal['fail_count'] += 1
                
            elif obj.ts_internal == 'YTS':
                dic_internal['yts_count'] += 1
                
            elif obj.ts_internal == 'In_progress':
                dic_internal['inprogress_count'] += 1
                
            elif obj.ts_internal == 'QA Skip':
                dic_internal['skip_count'] += 1
                
            elif obj.ts_internal == 'NA':
                dic_internal['na_count'] += 1


            
            if obj.ts_android == 'Pass':
                dic_android['pass_count'] += 1
            
            elif obj.ts_android == 'Fail':
                dic_android['fail_count'] += 1
                
            elif obj.ts_android == 'YTS':
                dic_android['yts_count'] += 1
                
            elif obj.ts_android == 'In_progress':
                dic_android['inprogress_count'] += 1
                
            elif obj.ts_android == 'QA Skip':
                dic_android['skip_count'] += 1
                
            elif obj.ts_android == 'NA':
                dic_android['na_count'] += 1


            
            if obj.ts_ios == 'Pass':
                dic_ios['pass_count'] += 1
            
            elif obj.ts_ios == 'Fail':
                dic_ios['fail_count'] += 1
                
            elif obj.ts_ios == 'YTS':
                dic_ios['yts_count'] += 1
                
            elif obj.ts_ios == 'In_progress':
                dic_ios['inprogress_count'] += 1
                
            elif obj.ts_ios == 'QA Skip':
                dic_ios['skip_count'] += 1
                
            elif obj.ts_ios == 'NA':
                dic_ios['na_count'] += 1


            
            if obj.ts_backend == 'Pass':
                dic_backend['pass_count'] += 1
            
            elif obj.ts_backend == 'Fail':
                dic_backend['fail_count'] += 1
                
            elif obj.ts_backend == 'YTS':
                dic_backend['yts_count'] += 1
                
            elif obj.ts_backend == 'In_progress':
                dic_backend['inprogress_count'] += 1
                
            elif obj.ts_backend == 'QA Skip':
                dic_backend['skip_count'] += 1
                
            elif obj.ts_backend == 'NA':
                dic_backend['na_count'] += 1


            
            if obj.ts_automation == 'Pass':
                dic_automation['pass_count'] += 1
            
            elif obj.ts_automation == 'Fail':
                dic_automation['fail_count'] += 1
                
            elif obj.ts_automation == 'YTS':
                dic_automation['yts_count'] += 1
                
            elif obj.ts_automation == 'In_progress':
                dic_automation['inprogress_count'] += 1
                
            elif obj.ts_automation == 'QA Skip':
                dic_automation['skip_count'] += 1
                
            elif obj.ts_automation == 'NA':
                dic_automation['na_count'] += 1


        mainlist.append(dic_portal)
        mainlist.append(dic_portal)
        mainlist.append(dic_portal)
        mainlist.append(dic_portal)
        mainlist.append(dic_portal)

        print("-------------------------------dataset--------------------")
        print(tcs)

        return render(request,"release_sheet.html",{'tcs':objs,
        'title':title,
        'users':users,
        'scope':scope,
        'dataset':tcs})
    else:
        return redirect('/')

def view_TCs(request,id):
    if 'email' in request.session and 'id' in request.session:
        users = User.objects.all()
        scope = Scope.objects.get(id = id)

        try:
            title = TestCase_Title.objects.get(scope_id = scope)
            obj = TestCase.objects.filter(title_id = title)
            print("-------------------Reached here-------------- and got------------" + str(obj))
            # for o in obj:
            #     print(o.tester_portal)
            #     print(o.tester_rm)
            #     if o.tester_internal is None:
            #         pass
            #     print(o.tester_be)
            #     print(o.tester_ios)
            #     print(o.tester_android)
            #     print(o.tester_automation)
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
            comment = request.POST.get('rcmnt')

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
        tc = TestCase.objects.get(id = id)
        scope = tc.title_id.scope_id
        tc.delete()
        return HttpResponseRedirect("/view_tcs/" + str(scope.id))

def logout(request):
    if 'email' in request.session and 'id' in request.session:
        del request.session['email']
        del request.session['uname']
        del request.session['id']
        return redirect('/')