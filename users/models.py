import uuid
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.mail import send_mail

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

    # 프로필 사진(사진을 uploads의 avatars 폴더에 저장)
    avatar = models.ImageField(upload_to="avatars", blank=True)
    # 성별
    gender = models.CharField(choices=GENDER_CHOICES, max_length=10, blank=True)
    # 소개
    bio = models.TextField(blank=True)
    # 생일
    birthday = models.DateField(blank=True, null=True)
    # 언어
    language = models.CharField(
        choices=LANGUAGE_CHOICES, max_length=2, blank=True, default=LANGUAGE_KOREAN
    )
    # 화폐(달러/원)
    currency = models.CharField(
        choices=CURRENCY_CHOICES, max_length=3, blank=True, default=CURRENCY_KRW
    )
    # superhost 여부(true/false)
    superhost = models.BooleanField(default=False)

    # default : 데이터베이스에 bio를 추가하면 필드가 모두 빈자리이므로 default값을 주어 해결
    # default값을 만들거나(default = ""), 비어있는 필드를 허용(null = True)

    email_verified = models.BooleanField(default=False)
    email_secret = models.CharField(max_length=20, default="", blank=True)

    def verify_email(self):

        if self.email_verified is False:
            secret = uuid.uuid4().hex[:20]  # hex : 16진수, [:20] : 20자리 만큼 채우기
            self.email_secret = secret

            send_mail(
                "Verify Airbnb Account",
                f"Verify account, this is your secret : {secret}",
                settings.EMAIL_FROM,
                [self.email,],
                fail_silently=False,
            )

        return
