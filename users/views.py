from django.contrib.auth import authenticate, login, logout
from django.db.models import Prefetch, Q
from django.shortcuts import get_object_or_404, redirect, render
from .forms import CustomUserCreationForm, ProfileForm, SkillForm
from .models import Profile
from projects.models import Project
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required

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
            messages.success(request, "Account created successfully 🎉 Please complete your profile to get started.")
            return redirect('edit-account')
            
    return render(request, 'users/register.html', {'form': form})

def logoutUser(request):
    logout(request)
    messages.success(request, "Logged out successfully")
    return redirect('login')

def profiles(request):
    users = Profile.objects.all()
    own_profile_id = None

    if request.user.is_authenticated and hasattr(request.user, 'profile'):
        own_profile_id = request.user.profile.id

    return render(
        request,
        'users/profiles.html',
        {
            'developers': users,
            'own_profile_id': own_profile_id,
        },
    )

def userProfile(request, pk):
    profile = get_object_or_404(
        Profile.objects.prefetch_related(
            'skill_set',
            Prefetch('project_set', queryset=Project.objects.prefetch_related('tags').order_by('-created')),
        ),
        id=pk,
    )

    if request.user.is_authenticated and hasattr(request.user, 'profile') and str(request.user.profile.id) == str(profile.id):
        return render(request, 'users/account.html', {'profile': profile})

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

@login_required(login_url='login')
def userAccount(request):
    profile = request.user.profile
    return render(request, 'users/account.html', {'profile': profile})

@login_required(login_url='login')
def editAccount(request):
    profile = request.user.profile
    form = ProfileForm(instance=profile)
    
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Your profile has been updated successfully ✨")
            return redirect('account')
        else:
            messages.error(request, "Please fix the errors below ❌")
    
    return render(request, 'users/profile_form.html', {'form': form})

@login_required(login_url='login')
def createSkill(request):
    form = SkillForm()
    profile = request.user.profile
    
    if request.method == 'POST':
        form = SkillForm(request.POST)
        if form.is_valid():
            skill = form.save(commit=False)
            skill.owner = profile
            skill.save()
            messages.success(request, "Skill added successfully. It is now part of your profile.")
            return redirect('account')
        
    return render(request, 'users/skill_form.html', {'form': form})
