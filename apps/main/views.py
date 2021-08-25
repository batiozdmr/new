from django.shortcuts import render
from django.db import transaction
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from apps.member_profile.models import UserProfile, Messages, UserGroup
from django.core.exceptions import ObjectDoesNotExist

from apps.main.models import TimeCounter,   ValueCounter, AnnouncementSection
from apps.parameter.models import   Menu, SubMenu, SiteSettings, Slider
from django.contrib.auth.models import User,Group
from apps.content.forms import PostForm
from apps.content.models import PostCreate, Event
from django.contrib import messages
from django.db.models import Q

def main(request):
    if request.user.is_authenticated:
        context = {}
        if request.method == "POST":
            form = PostForm(request.POST, request.FILES)

            if form.is_valid():
                content = form.cleaned_data.get("content")
                image = form.cleaned_data.get("image")
                video = form.cleaned_data.get("video")

                user = UserProfile.objects.get(user=request.user)

                newPost = PostCreate(text=user.user.first_name,user=user, content=content, image=image, video=video)
                newPost.save()
                messages.success(request, "Başarıyla Paylaşıldı.")

                return redirect('/')
        else:
            form = PostForm()
        context['form'] = form

        return render(request, "index.html", context)


    else:
        return redirect('/login/')




def menu(request):
    header_menu_list = Menu.objects.filter(menu_location_id=1).translate(
        request.LANGUAGE_CODE).order_by('alignment')
    footer_menu_list = Menu.objects.filter(menu_location_id=2).translate(
        request.LANGUAGE_CODE).order_by('alignment')
    left_menu_list = Menu.objects.filter(menu_location_id=3).translate(
        request.LANGUAGE_CODE).order_by('alignment')
    return {'header_menu_list': header_menu_list, 'footer_menu_list': footer_menu_list,
            'left_menu_list': left_menu_list}


def test(request):
    return render(request, "apps/competitions/competition_details.html")


def userprofile(request):
    if request.user.is_authenticated:
        user = request.user
        try:
            UserProfile.objects.get(user_id=user.id)
        except ObjectDoesNotExist:
            userProfile = UserProfile(user=user)
            userProfile.save()

        userprofile = UserProfile.objects.get(user_id=user.id)
        return {'userprofile': userprofile}
    else:
        return {'userprofile': ''}


def inbox(request):
    conversations = Messages.get_conversations(request.user)
    active_conversation = None
    messages = None
    if conversations:
        conversation = conversations[0]
        active_conversation = conversation['user'].username
        messages = Messages.objects.filter(user=request.user, conversation=conversation['user'])
        messages.update(is_read=True)
        for conversation in conversations:
            # bu kısımlar fonksiyon olur tekrar ediyor.
            if conversation['user'].username == active_conversation:
                conversation['unread'] = 0
            elif conversation['unread'] == 0:
                conversation['last_text'] = conversation['last_text']
            else:
                conversation['last_text'] = '<b style="color:black">' + conversation['last_text'] + '</b>'
        # en son konuşmanın okunmama sayısını 0 yaptık.

    return {
        'msgs': messages,
        'conversations': conversations,
        'active': active_conversation
    }


def members(request):
    all_groups = Group.objects.all()
    return render(request, "members/members.html", {'all_groups': all_groups})


def groups(request, name):
    if name == "all":
        group_user = UserProfile.objects.filter(~Q(user__groups=None))
        group_name = 'Tüm Gruplar'
    else:
        id_new = int(name)
        group_user = UserProfile.objects.filter(user__groups=id_new)
        group_name = Group.objects.get(id=id_new)
    return render(request, "members/members_archive.html", {'group_user': group_user, 'group_name': group_name})


