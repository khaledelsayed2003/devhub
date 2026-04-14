from .models import Project, Tag
from django.db.models import Q


def searchProjects(request):
    search_query = ''
    
    if request.GET.get('search_query_project'):
        search_query = request.GET.get('search_query_project')
        
    tags = Tag.objects.filter(name__icontains=search_query)
    
    projects_list = Project.objects.prefetch_related('tags').distinct().filter(
        Q(title__icontains=search_query) | Q(description__icontains=search_query) |
        Q(owner__name__icontains=search_query) | Q(tags__in=tags)).order_by('-created')
    
    return projects_list, search_query