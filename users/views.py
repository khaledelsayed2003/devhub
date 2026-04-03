from django.shortcuts import render
from .models import Profile

# Create your views here.

def profiles(request):
    users = Profile.objects.all()
    return render(request, 'users/profiles.html', {'developers': users})

def userProfile(request, pk):
    profile = Profile.objects.get(id=pk)

    topSkills = profile.skill_set.exclude(description__exact="")
    otherSkills = profile.skill_set.filter(description="")

    context = {
        'profile': profile,
        'topSkills': topSkills,
        'otherSkills': otherSkills
    }

    return render(request, 'users/user-profile.html', context)