from http.client import HTTPResponse
from django.shortcuts import render,HttpResponse

# Create your views here.
def home(request):
    return render(request,"home.html")



def login(request):
    return render(request,"login.html")


def signup(request):
    return render(request,"signup.html")


def cards(request):
    return render(request,"cards.html")

def cards(request):
    return render(request,"cards.html")