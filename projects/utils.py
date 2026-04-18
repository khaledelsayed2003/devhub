from .models import Project, Tag
from django.db.models import Q
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage


def paginateProjects(request, projects_list, results_per_page=4):
    page = request.GET.get('page')
    paginator = Paginator(projects_list, results_per_page)
    
    try:
        projects_list = paginator.page(page) 
    except PageNotAnInteger:
        projects_list = paginator.page(1) 
    except EmptyPage:
        projects_list = paginator.page(paginator.num_pages)
        
    return projects_list, paginator
    
    
def searchProjects(request):
    search_query = ''
    
    if request.GET.get('search_query_project'):
        search_query = request.GET.get('search_query_project')
        
    tags = Tag.objects.filter(name__icontains=search_query)
    
    projects_list = Project.objects.prefetch_related('tags').distinct().filter(
        Q(title__icontains=search_query) | Q(description__icontains=search_query) |
        Q(owner__name__icontains=search_query) | Q(tags__in=tags)).order_by('-created')
    
    return projects_list, search_query