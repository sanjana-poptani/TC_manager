from http.client import HTTPResponse
from django.shortcuts import redirect, render,HttpResponse
from django.contrib import messages

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

        if pwd != cpwd: 
            # return render(request,"signup.html",{'message':'Password and confirm password must be same!'})
            messages.error(request,"Password and confirm password must be same!")
            return redirect("signup")
    else:
        return render(request,"signup.html")


def cards(request):
    return render(request,"cards.html")

def releases(request):
    return render(request,"releases.html")

def release_sheet(request):
    return render(request,"release_sheet.html")