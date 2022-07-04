from http.client import HTTPResponse
from django.shortcuts import render,HttpResponse

# Create your views here.
def home(request):
    return HTTPResponse("<html><h1>Hey</h1></html>")