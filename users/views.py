from django.contrib.auth import authenticate, login, logout
from django.db.models import Prefetch, Q
from django.shortcuts import get_object_or_404, redirect, render
from .forms import CustomUserCreationForm
from .models import Profile
from projects.models import Project
from django.contrib.auth.models import User
from django.contrib import messages

# Create your views here.

def loginUser(request):
    
    if request.user.is_authenticated:
        return redirect('profiles')
    
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, f"Logged in successfully. Welcome back {user.username}")
            return redirect('profiles')
        else:
            messages.error(request, "Invalid username or password")

    return render(request, 'users/login.html')

def registerUser(request):
    form = CustomUserCreationForm()
    
    if request.user.is_authenticated:
        return redirect('profiles')
    
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            messages.success(request, "Account has been created successfully!")
            return redirect('profiles')
            
    return render(request, 'users/register.html', {'form': form})

def logoutUser(request):
    logout(request)
    messages.success(request, "Logged out successfully")
    return redirect('login')

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

def userAccount(request):
    return render(request, 'users/account.html')