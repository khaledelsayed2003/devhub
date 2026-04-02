from django.shortcuts import render
from .models import Profile

# Create your views here.

def profiles(request):
    users = Profile.objects.all()
    return render(request, 'users/profiles.html', {'developers': users})