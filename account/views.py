from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from .forms import LoginForm, UserEditForm, ProfileEditForm, CreateProfileForm
from .models import Profile


def user_login(request):
    if request.user.is_authenticated:
        return redirect("home:home")
    form = LoginForm()
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            user = User.objects.get(username=form.cleaned_data['username'])
            login(request, user)
            return redirect("home:home")

    return render(request, 'account/login.html', {'form': form})

def user_logout(request):
    logout(request)
    return redirect('home:home')

def user_register(request):
    if request.user.is_authenticated == True:
        return redirect("home:home")
    if request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password')
        password2 = request.POST.get('password2')
        if password1 == password2:
            user = User.objects.create_user(username=username, email=email, password=password1)
            return redirect('home:home')
        return render(request, 'account/register.html', {'error': 'different password'})
    return render(request, 'account/register.html', {})

def edit_profile(request):
    user = request.user
    try:
        profile = user.profile
    except Profile.DoesNotExist:
        return redirect('account:create_profile')

    if request.method == 'POST':
        user_form = UserEditForm(request.POST, instance=user)
        profile_form = ProfileEditForm(request.POST,request.FILES,instance=profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()

            return redirect('home:home')
    else:
        user_form = UserEditForm(instance=user)
        profile_form = ProfileEditForm(instance=profile)

    return render(request, 'account/edit.html', { 'user_form': user_form, 'profile_form': profile_form,})

@login_required
def create_profile(request):

    if Profile.objects.filter(user=request.user).exists():
        return redirect('account:edit')

    if request.method == 'POST':
        form = CreateProfileForm(request.POST,request.FILES )
        if form.is_valid():
            user = request.user
            user.first_name = form.cleaned_data['first_name']
            user.last_name = form.cleaned_data['last_name']
            user.save()
            Profile.objects.create(user=user,fathers_name=form.cleaned_data['fathers_name'],
                                   national_code=form.cleaned_data['national_code'],image=form.cleaned_data['image'])
            return redirect('account:edit')
    else:
        form = CreateProfileForm()

    return render(request,'account/create_profile.html',{'form': form})