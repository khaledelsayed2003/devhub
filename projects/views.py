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
    submitted_tag_names = set()

    for tag_name in newtags:
        tag_name = tag_name.strip()
        normalized_tag_name = tag_name.casefold()

        if not tag_name or normalized_tag_name in submitted_tag_names:
            continue

        tag = Tag.objects.filter(name__iexact=tag_name).order_by('-is_approved', 'created').first()
        if not tag:
            tag = Tag.objects.create(name=tag_name, is_approved=False)

        project.tags.add(tag)
        submitted_tag_names.add(normalized_tag_name)


def getCustomTagErrors(form, raw_tags):
    newtags = raw_tags.replace(',', " ").split()
    project_tag_names = {
        tag.name.casefold(): tag.name
        for tag in form.cleaned_data.get('tags', [])
    }
    submitted_tag_names = set()
    errors = []

    for tag_name in newtags:
        normalized_tag_name = tag_name.casefold()

        if normalized_tag_name in project_tag_names:
            errors.append(f"{project_tag_names[normalized_tag_name]} already exists in this project. Choose another tag.")
            continue

        if normalized_tag_name in submitted_tag_names:
            errors.append(f"{tag_name} was entered more than once. Keep each custom tag unique.")
            continue

        submitted_tag_names.add(normalized_tag_name)

    return errors


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
        newtags_errors = []
        form = ProjectForm(request.POST, request.FILES)
        if form.is_valid():
            newtags_errors = getCustomTagErrors(form, newtags)
            if not newtags_errors:
                project = form.save(commit=False)
                project.owner = profile
                project.save()
                form.save_m2m()
                addCustomTags(project, newtags)
                messages.success(request, "Project created successfully. Your work is now live on DevHub.")
                return redirect(f"{reverse('projects')}#project-{project.id}")
            messages.error(request, newtags_errors[0])
    else:
        form = ProjectForm()
        newtags_errors = []
    
    return render(request, 'projects/project_form.html', {'form': form, 'is_update': False, 'newtags_errors': newtags_errors})

@login_required(login_url='login')
def updateProject(request, pk):
    profile = request.user.profile
    project = profile.project_set.get(id=pk)
    if request.method == 'POST':
        newtags = request.POST.get('newtags', '')
        newtags_errors = []
        form = ProjectForm(request.POST, request.FILES, instance=project)
        if form.is_valid():
            newtags_errors = getCustomTagErrors(form, newtags)
            if not newtags_errors:
                project = form.save()
                addCustomTags(project, newtags)
                messages.success(request, "Project updated successfully. Your latest changes are now live.")
                return redirect('account')
            messages.error(request, newtags_errors[0])
    else:
        form = ProjectForm(instance=project)
        newtags_errors = []
    
    return render(request, 'projects/project_form.html', {'form': form, 'is_update': True, 'newtags_errors': newtags_errors})

@login_required(login_url='login')
def deleteProject(request, pk):
    profile = request.user.profile
    project = profile.project_set.get(id=pk)
    if request.method == 'POST':
        project.delete()
        messages.success(request, "Project deleted successfully. It is no longer visible on your profile.")
        return redirect('account')
    
    return render(request, 'projects/delete_project.html', {'project': project})
