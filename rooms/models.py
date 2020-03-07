from django.db import models  # django와 관련된 것들
from django_countries.fields import CountryField  # 외부 패키지
from core import models as core_models  # 내가 만든 패키지
from users import models as user_models

# Create your models here.


class AbstractItem(core_models.TimeStampedModel):

    """ Abstract Item """

    name = models.CharField(max_length=80)

    class Meta:
        abstract = True

    def __str__(self):
        return self.name


class RoomType(AbstractItem):
    pass


class Room(core_models.TimeStampedModel):

    """ Room Model Definition """

    name = models.CharField(max_length=140)  # 방 이름(필수 입력)
    description = models.TextField()  # 방 설명
    country = CountryField()  # 위치한 나라
    city = models.CharField(max_length=80)  # 위치한 도시
    price = models.IntegerField()  # 가격
    address = models.CharField(max_length=140)
    guests = models.IntegerField()  # 인원 수

    beds = models.IntegerField()  # 침대 수
    bedrooms = models.IntegerField()  # 침실 수
    baths = models.IntegerField()  # 화장실 수

    check_in = models.TimeField()  # 체크인
    check_out = models.TimeField()  # 체크아웃
    instant_book = models.BooleanField(default=False)  # 즉시 예약

    host = models.ForeignKey(user_models.User, on_delete=models.CASCADE)
    # room에서 host field와 user field(user의 id) 연결
    # ForeignKey : 한 모델을 다른 모델과 연결시킴
    # many-to-one(일대다 관계) : rooms는 한 명의 host를 가질 수 있음

    room_type = models.ManyToManyField(RoomType, blank=True)
    # many-to-many(다대다 관계) : room type은 여러 개를 가질 수 있음

    def __str__(self):
        return self.name  # 방 이름을 보이게 함(Room object 대신)

