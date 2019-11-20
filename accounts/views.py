from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login as auth_login, logout as auth_logout
from django.contrib.auth.forms import AuthenticationForm
from .models import User
from .forms import CustomUserCreationForm
# Create your views here.


def userlist(request):
    users = User.objects.all()
    context = {'users': users}
    return render(request, 'accounts/userlist.html', context)


def userdetail(request, user_pk):
    user = get_object_or_404(User, pk=user_pk)
    context = {'user': user}
    return render(request, 'accounts/userdetail.html', context)


def signup(request):
    if request.user.is_authenticated:
        return redirect('accounts:userlist')
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            return redirect('accounts:userlist')
    else:
        form = CustomUserCreationForm()
    context = {'form': form}
    return render(request, 'accounts/auth_form.html', context)


def login(request):
    if request.user.is_authenticated:
        return redirect('accounts:userlist')
    if request.method == "POST":
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            auth_login(request, form.get_user())
            return redirect(request.GET.get('next') or 'accounts:userlist')
    else:
        form = AuthenticationForm()
    context = {'form': form}
    return render(request, 'accounts/auth_form.html', context)


def logout(request):
    auth_logout(request)
    return redirect('accounts:userlist')
