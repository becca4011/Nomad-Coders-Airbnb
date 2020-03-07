from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
# model : 데이터가 보여지는 모습


class User(AbstractUser):  # 상속

    """ Custom User Model """

    GENDER_MALE = "male"
    GENDER_FEMALE = "female"
    GENDER_OTHER = "other"

    GENDER_CHOICES = (
        (GENDER_MALE, "Male"),
        (GENDER_FEMALE, "Female"),
        (GENDER_OTHER, "Other"),
    )

    LANGUAGE_ENGLISH = "en"
    LANGUAGE_KOREAN = "kr"

    LANGUAGE_CHOICES = ((LANGUAGE_ENGLISH, "English"), (LANGUAGE_KOREAN, "Korean"))

    CURRENCY_USD = "usd"
    CURRENCY_KRW = "krw"

    CURRENCY_CHOICES = ((CURRENCY_USD, "USD"), (CURRENCY_KRW, "KRU"))

    # 프로필 사진
    avatar = models.ImageField(blank=True)
    # 성별
    gender = models.CharField(choices=GENDER_CHOICES, max_length=10, blank=True)
    # 소개
    bio = models.TextField(blank=True)
    # 생일
    birthday = models.DateField(blank=True, null=True)  # 언어
    language = models.CharField(choices=LANGUAGE_CHOICES, max_length=2, blank=True)
    # 화폐(달러/원)
    currency = models.CharField(choices=CURRENCY_CHOICES, max_length=3, blank=True)
    # superhost 여부(true/false)
    superhost = models.BooleanField(default=False)

    # default : 데이터베이스에 bio를 추가하면 필드가 모두 빈자리이므로 default값을 주어 해결
    # default값을 만들거나(default = ""), 비어있는 필드를 허용(null = True)

