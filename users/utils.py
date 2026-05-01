from .models import Profile, Skill
from django.db.models import Q
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage


def paginateProfiles(request, profiles, results_per_page=3):
    page = request.GET.get('page')
    paginator = Paginator(profiles, results_per_page)

    try:
        profiles = paginator.page(page)
    except PageNotAnInteger:
        profiles = paginator.page(1)
    except EmptyPage:
        profiles = paginator.page(paginator.num_pages)

    return profiles, paginator


def searchProfiles(request):
    search_query = ''
    
    if request.GET.get('search_query_developer'):
        search_query = request.GET.get('search_query_developer')
        
    skills = Skill.objects.filter(name__icontains=search_query)
    users = Profile.objects.distinct().filter(
        Q(name__icontains=search_query) | Q(short_intro__icontains=search_query) | Q(skill__in=skills)).order_by('-created')
    
    return users, search_query
