from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Project
from .forms import ProjectForm

def home(request):
    return render(request, 'base.html')

def projects(request):
    projects_list = Project.objects.prefetch_related('tags').all().order_by('-created')
    featured_project = (
        Project.objects.prefetch_related('tags')
        .order_by('-vote_total', '-vote_ratio', '-created')
        .first()
    )
    return render(
        request,
        'projects/projects.html',
        {
            'projects': projects_list,
            'featured_project': featured_project,
        }
    )

def project(request, pk):
    projectObj = Project.objects.get(id=pk)
    return render(request, 'projects/single-project.html', {'project': projectObj})

def createProject(request):
    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('projects')
    else:
        form = ProjectForm()
    
    return render(request, 'projects/project_form.html', {'form': form})

def updateProject(request, pk):
    project = Project.objects.get(id=pk)
    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES, instance=project)
        if form.is_valid():
            form.save()
            return redirect('projects')
    else:
        form = ProjectForm(instance=project)
    
    return render(request, 'projects/project_form.html', {'form': form})

def deleteProject(request, pk):
    project = Project.objects.get(id=pk)
    if request.method == 'POST':
        project.delete()
        return redirect('projects')
    
    return render(request, 'projects/delete_project.html', {'project': project})
