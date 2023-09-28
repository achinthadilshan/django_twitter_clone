from django.shortcuts import render, redirect
from django.contrib import messages
from .models import *

# Create your views here.


def home(request):
    context = {}
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
        context = {"profile": profile}
        return render(request, 'profile.html', context)
    else:
        messages.success(request, ('You must be logged in to view this page!'))
        return redirect('home')
