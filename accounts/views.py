from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from .forms import CustomUserCreationForm
from .models import User

# Create your views here.
def signup(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('accounts:login')
    else:
        form = CustomUserCreationForm()
    context = {
        'form': form
    }
    return render(request, 'accounts/form.html', context)

def login(request):
    if request.method == "POST":
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            auth_login(request, form.get_user())
            return redirect('posts:index')
    else:
        form = AuthenticationForm()
    context = {
        'form': form
    }
    return render(request, 'accounts/form.html', context)

def logout(request):
    auth_logout(request)
    return redirect("accounts:login")

def user_page(request, id):
    user_info = get_object_or_404(User, id=id)
    context = {
        'user_info': user_info
    }
    return render(request, 'accounts/user_page.html', context)

def follow(request, id):
    you = get_object_or_404(User, id=id)
    me = request.user
    # 내가 나를 팔로우할 수 없도록
    if you != me:
        if you in me.followings.all():
            me.followings.remove(you)
            # you.followers.remove(me)
        else:
            me.followings.add(you)
            # you.followers.add(me)
    return redirect('accounts:user_page', id)
