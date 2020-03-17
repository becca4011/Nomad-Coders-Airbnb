from django.utils import timezone
from django.views.generic import ListView
from . import models

# Create your views here.


class HomeView(ListView):

    """ HomeView Definition """

    model = models.Room

    paginate_by = 10
    paginate_orphans = 5  # orphans : 마지막 페이지의 객실 수가 5개 이하면 이전 페이지에 마지막 페이지의 객실을 넣음
    ordering = "created"  # 정렬방식
    context_object_name = "rooms"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        now = timezone.now()
        context["now"] = now

        return context
