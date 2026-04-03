from django.db.models import Prefetch, Q
from django.shortcuts import get_object_or_404, render
from .models import Profile
from projects.models import Project

# Create your views here.

def profiles(request):
    users = Profile.objects.all()
    return render(request, 'users/profiles.html', {'developers': users})

def userProfile(request, pk):
    profile = get_object_or_404(
        Profile.objects.prefetch_related(
            'skill_set',
            Prefetch('project_set', queryset=Project.objects.prefetch_related('tags').order_by('-created')),
        ),
        id=pk,
    )

    topSkills = profile.skill_set.exclude(description__isnull=True).exclude(description__exact="")
    otherSkills = profile.skill_set.filter(Q(description__isnull=True) | Q(description=""))
    projects = profile.project_set.all()

    context = {
        'profile': profile,
        'topSkills': topSkills,
        'otherSkills': otherSkills,
        'projects': projects,
    }

    return render(request, 'users/user-profile.html', context)
