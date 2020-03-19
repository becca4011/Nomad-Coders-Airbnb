from django.views.generic import ListView, DetailView
from django.shortcuts import render
from . import models

# Create your views here.


class HomeView(ListView):

    """ HomeView Definition """

    model = models.Room

    paginate_by = 10
    paginate_orphans = 5  # orphans : 마지막 페이지의 객실 수가 5개 이하면 이전 페이지에 마지막 페이지의 객실을 넣음
    ordering = "created"  # 정렬방식
    context_object_name = "rooms"


class RoomDetail(DetailView):

    """ RoomDetail Definition """

    model = models.Room


def search(request):
    city = request.GET.get("city")
    city = str.capitalize(city)
    return render(request, "rooms/search.html", {"city": city})
