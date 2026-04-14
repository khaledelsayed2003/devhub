from .models import Profile, Skill
from django.db.models import Q


def searchProfiles(request):
    search_query = ''
    
    if request.GET.get('search_query_developer'):
        search_query = request.GET.get('search_query_developer')
        
    skills = Skill.objects.filter(name__icontains=search_query)
    users = Profile.objects.distinct().filter(
        Q(name__icontains=search_query) | Q(short_intro__icontains=search_query) | Q(skill__in=skills))
    
    return users, search_query