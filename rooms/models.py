from django.db import models  # django와 관련된 것들
from django.urls import reverse
from django_countries.fields import CountryField  # 외부 패키지
from core import models as core_models  # 내가 만든 패키지

# Create your models here.


class AbstractItem(core_models.TimeStampedModel):

    """ Abstract Item """

    name = models.CharField(max_length=80)

    class Meta:
        abstract = True

    def __str__(self):
        return self.name


class Photo(core_models.TimeStampedModel):

    """ Photo Model Definition """

    caption = models.CharField(max_length=80)
    file = models.ImageField(upload_to="room_photos")  # 사진을 uploads의 room_photos에 저장
    room = models.ForeignKey("Room", related_name="photos", on_delete=models.CASCADE)
    # ForeignKey : Room과 Photo를 연결
    # on_delete=models.CASCADE : 방이 지워지면 사진도 같이 지워져야 하기 때문에 사용

    def __str__(self):
        return self.caption


class RoomType(AbstractItem):  # 방 유형

    """ RoomType Model Definition """

    class Meta:
        verbose_name = "Room Type"  # verbose_name : class 이름이 아닌 원하는 이름으로 바꿀 수 있음


class Amenity(AbstractItem):  # 편의시설

    """ Amenity Model Definition """

    class Meta:
        verbose_name_plural = (
            "Amenities"  # verbose_name_plural : django는 class 이름에 s를 붙이는데, 그것을 방지
        )


class Facility(AbstractItem):  # 시설

    """ Facility Model Definition """

    class Meta:
        verbose_name_plural = "Facilities"


class HouseRule(AbstractItem):  # 규칙

    """ HouseRule Model Definition """

    class Meta:
        verbose_name = "House Rule"


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

    host = models.ForeignKey(
        "users.User", related_name="rooms", on_delete=models.CASCADE
    )
    # room에서 host field와 user field(user의 id) 연결
    # ForeignKey : 한 모델을 다른 모델과 연결시킴
    # many-to-one(일대다 관계) : rooms는 한 명의 host를 가질 수 있음
    # on_delete=models.CASCADE : User를 삭제하면 User가 등록한 Room도 삭제(cascade = 폭포수)

    room_type = models.ForeignKey(
        "RoomType", related_name="rooms", on_delete=models.SET_NULL, null=True
    )
    # 방 유형을 한 가지만 선택 가능하게 함

    amenities = models.ManyToManyField("Amenity", related_name="rooms", blank=True)
    facilities = models.ManyToManyField("Facility", related_name="rooms", blank=True)
    house_rules = models.ManyToManyField("HouseRule", related_name="rooms", blank=True)
    # many-to-many(다대다 관계) : room type은 여러 개를 가질 수 있음

    def __str__(self):
        return self.name  # 방 이름을 보이게 함(Room object 대신)

    def save(self, *args, **kwargs):
        self.city = str.capitalize(self.city)  # 앞글자를 대문자로 바꿈
        super().save(*args, **kwargs)  # 실제 save method 호출

    def get_absolute_url(
        self,
    ):  # admin에서 만든 방이 웹사이트에서 어떻게 보이는지 확인할 수 있게 함(view on site 버튼)
        return reverse("rooms:detail", kwargs={"pk": self.pk})

    def total_rating(self):
        all_reviews = self.reviews.all()
        all_ratings = 0

        if len(all_reviews) > 0:
            for review in all_reviews:
                all_ratings += review.rating_average()

            return round(all_ratings / len(all_reviews), 2)

        return 0

