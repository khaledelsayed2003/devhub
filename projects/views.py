from django.shortcuts import render
from django.http import HttpResponse


def projects(request):
    return HttpResponse("Here you can find the projects")

def project(request):
    return HttpResponse("Here is a single project!")