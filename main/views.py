from django.shortcuts import render

from .models import *

# Create your views here.


def home(request):
    context = {}
    return render(request, 'home.html', context)


def profile_list(request):
    profiles = Profile.objects.exclude(user=request.user)
    context = {"profiles": profiles}
    return render(request, 'profile_list.html', context)
