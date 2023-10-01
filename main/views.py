from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .models import *
from .forms import *
from django.contrib.auth.forms import UserCreationForm
from django import forms

# Create your views here.


def home(request):
    if request.user.is_authenticated:
        form = TweetForm(request.POST or None)
        if request.method == "POST":
            if form.is_valid():
                tweet = form.save(commit=False)
                tweet.user = request.user
                tweet.save()
                messages.success(request, ('Your tweet has been posted!'))
                return redirect('home')

        tweets = Tweet.objects.all().order_by("-created_at")
        context = {"tweets": tweets, "form": form}
        return render(request, 'home.html', context)
    else:
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


def login_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, ('You have been logged in!'))
            return redirect('home')
        else:
            messages.success(request, ('Couldn\'t find an user!'))
            return redirect('login')
    else:
        if request.user.is_authenticated:
            messages.success(request, ('You\'re already logged in!'))
            return redirect('home')
        else:
            return render(request, 'login.html')


def logout_user(request):
    logout(request)
    messages.success(request, ('You have been logged out!'))
    return redirect('home')


def register_user(request):
    form = SignUpForm()
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']

            # Additional
            # first_name = form.cleaned_data['first_name']
            # last_name = form.cleaned_data['last_name']
            # email = form.cleaned_data['email']

            # login user
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, ('You have successfully registered!'))
            return redirect('home')
    else:
        if request.user.is_authenticated:
            messages.success(request, ('You\'re already registered!'))
            return redirect('home')
        else:
            context = {"form": form}
            return render(request, 'register.html', context)
