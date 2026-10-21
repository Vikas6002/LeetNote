# accounts/views.py
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import RegisterForm, ProfileForm
from .models import UserProfile


def register_view(request):
    if request.user.is_authenticated:
        return redirect('notes:list')

    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            # create a profile for the new user automatically
            UserProfile.objects.create(user=user)
            login(request, user)
            messages.success(request, f"Welcome {user.username}! Start adding your notes.")
            return redirect('notes:list')
    else:
        form = RegisterForm()

    return render(request, 'accounts/register.html', {'form': form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect('notes:list')

    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            # go to next page if redirected from login_required
            next_url = request.GET.get('next', 'notes:list')
            return redirect(next_url)
        else:
            messages.error(request, "Invalid username or password.")
    else:
        form = AuthenticationForm()

    return render(request, 'accounts/login.html', {'form': form})


def logout_view(request):
    if request.method == 'POST':
        logout(request)
        return redirect('accounts:login')
    return redirect('accounts:login')


@login_required
def profile_view(request):
    profile, _ = UserProfile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated.")
            return redirect('accounts:profile')
    else:
        form = ProfileForm(instance=profile)

    # stats to show on profile page
    total_notes = request.user.notes.count()
    easy_count  = request.user.notes.filter(difficulty='easy').count()
    medium_count= request.user.notes.filter(difficulty='medium').count()
    hard_count  = request.user.notes.filter(difficulty='hard').count()

    context = {
        'form'        : form,
        'profile'     : profile,
        'total_notes' : total_notes,
        'easy_count'  : easy_count,
        'medium_count': medium_count,
        'hard_count'  : hard_count,
    }
    return render(request, 'accounts/profile.html', context)