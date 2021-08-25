from django.shortcuts import render
from django.db import transaction
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from apps.member_profile.models import UserProfile
from django.core.exceptions import ObjectDoesNotExist
from apps.main.models import TimeCounter,   ValueCounter, AnnouncementSection
from apps.parameter.models import SiteSettings


def site_settings(request):
    site_setting = SiteSettings.objects.all().last()
    return {'site_setting': site_setting}


