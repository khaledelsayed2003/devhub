from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Project
from .forms import ProjectForm
from django.contrib.auth.decorators import login_required


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

@login_required(login_url='login')
def createProject(request):
    profile = request.user.profile
    
    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES)
        if form.is_valid():
            project = form.save(commit=False)
            project.owner = profile
            project.save()
            return redirect('projects')
    else:
        form = ProjectForm()
    
    return render(request, 'projects/project_form.html', {'form': form})

@login_required(login_url='login')
def updateProject(request, pk):
    profile = request.user.profile
    project = profile.project_set.get(id=pk)
    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES, instance=project)
        if form.is_valid():
            form.save()
            return redirect('projects')
    else:
        form = ProjectForm(instance=project)
    
    return render(request, 'projects/project_form.html', {'form': form})

@login_required(login_url='login')
def deleteProject(request, pk):
    profile = request.user.profile
    project = profile.project_set.get(id=pk)
    if request.method == 'POST':
        project.delete()
        return redirect('projects')
    
    return render(request, 'projects/delete_project.html', {'project': project})
