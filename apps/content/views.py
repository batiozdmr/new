from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, redirect
from apps.member_profile.models import UserProfile, Follow, UserGroup
from .models import PostCreate, Event
from datetime import date
from calendar import calendar
import calendar
# Create your views here.
from datetime import datetime, date, timedelta
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.views import generic
from django.utils.safestring import mark_safe
from django.db.models import Q
from .forms import EventForm
from .models import *
from .utils import Calendar
from apps.member_profile.models import Achievement, AchievementCategorie
from django.db.models import Count
# Create your views here.


def shared_post(request):
    postArray = []
    if request.user.is_authenticated:
        user = request.user
        profile_id = UserProfile.objects.get(id=user.id)
        try:
            user_object = Follow.objects.all().filter(following_user_id=profile_id.id)
            posts = PostCreate.objects.all().order_by('-created_at')

            for post in posts:
                if post.user.user_id == user.id:
                    postArray.append(post)
                for users in user_object:
                    if post.user.user_id == users.followed_user_id  :
                        postArray.append(post)


        except ObjectDoesNotExist:
            postArray = []
    post_size = len(postArray)
    return {'postArray': postArray, 'post_size': post_size}


def Message(request):
    user = request.user

    return {'message': user}


def events(request):
    if request.user.is_authenticated:
        today_date = date.today()
        month = int(today_date.month)
        event = Event.objects.filter(start_time__month=month)
        return {'events': event}
    return {'events': ''}


def leaderboard(request):
    user = request.user
    user_point = UserProfile.objects.get(id=user.id)
    users = UserProfile.objects.all()
    for i in users:
        i.total_point = i.point()
        i.save()
    ordered = UserProfile.objects.order_by('-total_point')
    others = ordered[3:6]

    return render(request, "leaderboard/leaderboard.html", {'user_point' : user_point,  'others':others ,'ordered':ordered})



class CalendarView(generic.ListView):
    model = Event
    template_name = 'calendar/takvim.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # use today's date for the calendar
        d = get_date(self.request.GET.get('day', None))

        # Instantiate our calendar class with today's year and date
        cal = Calendar(d.year, d.month)

        # Call the formatmonth method, which returns our calendar as a table
        html_cal = cal.formatmonth(withyear=True)
        context['calendar'] = mark_safe(html_cal)
        d = get_date(self.request.GET.get('month', None))
        context['prev_month'] = prev_month(d)
        context['next_month'] = next_month(d)

        return context


def prev_month(d):
    first = d.replace(day=1)
    prev_month = first - timedelta(days=1)
    month = 'month=' + str(prev_month.year) + '-' + str(prev_month.month)
    return month


def next_month(d):
    days_in_month = calendar.monthrange(d.year, d.month)[1]
    last = d.replace(day=days_in_month)
    next_month = last + timedelta(days=1)
    month = 'month=' + str(next_month.year) + '-' + str(next_month.month)
    return month


def get_date(req_day):
    if req_day:
        year, month = (int(x) for x in req_day.split('-'))
        return date(year, month, day=1)
    return datetime.today()


def event(request, event_id=None):
    instance = Event()
    if event_id:
        instance = get_object_or_404(Event, pk=event_id)
    else:
        instance = Event()

    form = EventForm(request.POST, request.FILES)
    if request.POST and form.is_valid():
        form.save()
        return HttpResponseRedirect(reverse('content:takvim'))
    return render(request, 'calendar/event.html', {'form': form})


def user_search(request):
    search_query = request.GET.get('q')
    if search_query:
        user_list = UserProfile.objects.filter(Q(user__username__icontains=search_query) |
                                               Q(user__first_name__icontains=search_query) |
                                               Q(user__last_name__icontains=search_query)).distinct()[:4]

        event_list = Event.objects.filter(Q(title__icontains=search_query) |
                                          Q(description__icontains=search_query)).distinct()[:4]
        group_list = UserGroup.objects.filter(Q(text__icontains=search_query) |
                                              Q(explanation__icontains=search_query)).distinct()[:4]
        forum_list = Forum.objects.filter( Q(question__icontains=search_query)).distinct()[:4]

    return render(request, "search/search.html", {'user_list': user_list, 'event_list': event_list,'group_list':group_list, 'forum_list': forum_list })


def forum(request):

    forums = Forum.objects.all()
    for forum in forums:
        forum.answer_size = forum.size()
        forum.save()

    forum_category = ForumCategory.objects.all()


    return render(request,"forum/forum.html", {'forum_category':forum_category })

