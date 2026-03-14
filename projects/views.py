from django.shortcuts import render
from django.http import HttpResponse
from .models import Project



def projects(request):
    projectsList = Project.objects.all()
    return render(request, 'projects/projects.html', {'projects': projectsList})

def project(request, pk):
    projectObj = Project.objects.get(id=pk)
    return render(request, 'projects/single-project.html', {'project': projectObj})

def createProject(request):
    return render(request, 'projects/project_form.html')