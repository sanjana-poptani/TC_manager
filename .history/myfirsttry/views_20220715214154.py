from http.client import HTTPResponse
from django.shortcuts import render,HttpResponse

# Create your views here.
def home(request):
    return render(request,"home.html")



def login(request):
    return render(request,"login.html")


def signup(request):
    if request.method == 'POST':
        username = request.POST.get('')
    return render(request,"signup.html")


def cards(request):
    return render(request,"cards.html")

def releases(request):
    return render(request,"releases.html")

def release_sheet(request):
    return render(request,"release_sheet.html")