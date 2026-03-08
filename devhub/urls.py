from django.contrib import admin
from django.urls import path
from django.http import HttpResponse

def projects(request):
    return HttpResponse("Here you can find the projects")

def project(request):
    return HttpResponse("Here is a single project!")

urlpatterns = [
    path('admin/', admin.site.urls),
    path('projects/', projects, name='projects'),
    path('project/', project, name='project')
]
