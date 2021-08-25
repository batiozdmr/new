from django.shortcuts import render
from django.views.generic import CreateView

from .form import RegisterForm, ProfileForm, SectorApplicationForm
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, redirect
from .models import UserProfile, UserGroup, SectorCategory, Sector
from apps.content.views import PostCreate


# Create your views here.


def userprofile(request):
    return {'username': request.user.username}


def register(request):
    form = RegisterForm(request.POST or None)
    if form.is_valid():
        name = form.cleaned_data.get("name")
        surname = form.cleaned_data.get("surname")
        e_mail = form.cleaned_data.get("e_mail")
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")
        try:
            UserControl = User.objects.get(username=username)
        except ObjectDoesNotExist:
            UserControl = None

        if UserControl == None:
            newUser = User.objects.create_user(username=username, first_name=name.capitalize(), last_name=surname.capitalize(), email=e_mail,
                                               password=password)
            newUser.save()
            userProfile = UserProfile(user=newUser)
            userProfile.save()
            return redirect('/login/')

    context = {
        "form": form
    }
    return render(request, "registration/register.html", context)


def profile(request):
    user = request.user
    user_profile = UserProfile.objects.get(user=user)
    post = PostCreate.objects.filter(user__user=user).order_by('-id')[:3]
    teams = UserGroup.objects.filter(user__user=user)

    return render(request, "profile/profile.html", {'profile': user_profile, 'posts': post, 'teams': teams})


def profil_edit(request):
    form = ProfileForm()
    return render(request, "profile/profile_edit.html", {'form': form})


def sector(request):
    context = {}
    if request.method == "POST":
        form = SectorApplicationForm(request.POST or None)
        if form.is_valid():
            form.save()
    else:
        form = SectorApplicationForm()
    context['form'] = form

    return render(request, "profile/sector_category.html", context)


