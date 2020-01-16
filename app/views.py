from django.shortcuts import render
from django.shortcuts import HttpResponse, HttpResponsePermanentRedirect

def index(request):
    return HttpResponse("Index page!")