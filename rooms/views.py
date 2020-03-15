from django.shortcuts import render
from . import models

# Create your views here.


def all_rooms(request):  # core의 urls.py의 이름과 같아야 함
    all_rooms = models.Room.objects.all()
    return render(request, "rooms/home.html", context={"rooms": all_rooms})
    # templates 안의 html 파일 이름과 같아야 함
    # 템플릿 안의 이름과 context의 이름이 같아야 함(home.html의 rooms)
