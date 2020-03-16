from math import ceil
from django.shortcuts import render
from . import models

# Create your views here.


def all_rooms(request):  # core의 urls.py의 이름과 같아야 함
    page = request.GET.get("page", 1)
    page = int(page or 1)
    page_size = 10

    limit = page_size * page
    offset = limit - page_size
    all_rooms = models.Room.objects.all()[offset:limit]
    page_count = ceil(models.Room.objects.count() / page_size)

    return render(
        request,
        "rooms/home.html",
        context={
            "rooms": all_rooms,
            "page": page,
            "page_count": page_count,
            "page_range": range(1, page_count),
        },
    )

    # [0:10] : 0(offset) ~ 10(limit)번까지 보여줌 / [10:20] : 10 ~ 20번까지 보여줌
    # templates 안의 html 파일 이름과 같아야 함
    # 템플릿 안의 이름과 context의 이름이 같아야 함(home.html의 rooms)
