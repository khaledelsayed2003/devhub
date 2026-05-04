from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Project, Tag
from .forms import ProjectForm, ReviewForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse
from django.db.models import Q
from .utils import searchProjects, paginateProjects


def addCustomTags(project, raw_tags):
    newtags = raw_tags.replace(',', " ").split()

    for tag_name in newtags:
        tag, created = Tag.objects.get_or_create(
            name=tag_name,
            defaults={'is_approved': False}
        )
        project.tags.add(tag)


def projects(request):
    projects_list, search_query = searchProjects(request)
    projects_list, paginator = paginateProjects(request, projects_list, 4)
    
    featured_project = (
        Project.objects.prefetch_related('tags').filter(
            vote_total__gte=10
        ).order_by('-vote_ratio', '-vote_total', '-created')
        .first()
        or Project.objects.prefetch_related('tags').order_by('-vote_ratio', '-vote_total', '-created').first()
    )
    
    return render(
        request,
        'projects/projects.html',
        {
            'projects': projects_list,
            'featured_project': featured_project,
            'search_query' : search_query,
            'paginator' : paginator,
        }
    )

def project(request, pk):
    projectObj = Project.objects.get(id=pk)
    reviews = projectObj.review_set.all().order_by('-created')
    form = ReviewForm()
    
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        review = form.save(commit=False)
        review.project = projectObj
        review.owner = request.user.profile
        review.save()
        projectObj.getVoteCount
        messages.success(request, "Review submitted successfully for this project")
        return redirect('project', pk=projectObj.id)

    
    return render(request, 'projects/single-project.html', {'project': projectObj, 'reviews': reviews, 'form': form})

def createProject(request):
    if not request.user.is_authenticated:
        messages.warning(request, "Please log in to post a project.")
        return redirect(f"{reverse('login')}?next={request.path}")
    
    profile = request.user.profile
    
    if request.method == 'POST':
        newtags = request.POST.get('newtags', '')
        form = ProjectForm(request.POST, request.FILES)
        if form.is_valid():
            project = form.save(commit=False)
            project.owner = profile
            project.save()
            form.save_m2m()
            addCustomTags(project, newtags)
            messages.success(request, "Project created successfully. Your work is now live on DevHub.")
            return redirect(f"{reverse('projects')}#project-{project.id}")
    else:
        form = ProjectForm()
    
    return render(request, 'projects/project_form.html', {'form': form, 'is_update': False})

@login_required(login_url='login')
def updateProject(request, pk):
    profile = request.user.profile
    project = profile.project_set.get(id=pk)
    if request.method == 'POST':
        newtags = request.POST.get('newtags', '')
        form = ProjectForm(request.POST, request.FILES, instance=project)
        if form.is_valid():
            project = form.save()
            addCustomTags(project, newtags)
            messages.success(request, "Project updated successfully. Your latest changes are now live.")
            return redirect('account')
    else:
        form = ProjectForm(instance=project)
    
    return render(request, 'projects/project_form.html', {'form': form, 'is_update': True})

@login_required(login_url='login')
def deleteProject(request, pk):
    profile = request.user.profile
    project = profile.project_set.get(id=pk)
    if request.method == 'POST':
        project.delete()
        messages.success(request, "Project deleted successfully. It is no longer visible on your profile.")
        return redirect('account')
    
    return render(request, 'projects/delete_project.html', {'project': project})
