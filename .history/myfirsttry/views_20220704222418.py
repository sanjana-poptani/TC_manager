from http.client import HTTPResponse
from django.shortcuts import render,HttpResponse

# Create your views here.
def home(request):
    return render(request,"home.html")



def home(request):
    return render(request,"home.html")