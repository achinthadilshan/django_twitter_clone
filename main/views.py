from django.shortcuts import render, redirect
from django.contrib import messages
from .models import *

# Create your views here.


def home(request):
    if request.user.is_authenticated:
        tweets = Tweet.objects.all().order_by("-created_at")

    context = {"tweets": tweets}
    return render(request, 'home.html', context)


def profile_list(request):
    if request.user.is_authenticated:
        profiles = Profile.objects.exclude(user=request.user)
        context = {"profiles": profiles}
        return render(request, 'profile_list.html', context)
    else:
        messages.success(request, ('You must be logged in to view this page!'))
        return redirect('home')


def profile(request, pk):
    if request.user.is_authenticated:
        profile = Profile.objects.get(user_id=pk)
        tweets = Tweet.objects.filter(user_id=pk).order_by("-created_at")

        # POST form logic
        if request.method == 'POST':
            # Get current user
            current_user_profile = request.user.profile
            # Get form data
            action = request.POST['follow']
            # Decide follow or unfollow
            if action == 'unfollow':
                current_user_profile.follows.remove(profile)
            elif action == 'follow':
                current_user_profile.follows.add(profile)

            # Save the profile
            current_user_profile.save()

        context = {"profile": profile, "tweets": tweets}
        return render(request, 'profile.html', context)
    else:
        messages.success(request, ('You must be logged in to view this page!'))
        return redirect('home')
