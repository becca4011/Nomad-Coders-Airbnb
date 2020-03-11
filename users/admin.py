from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from . import models  # admin.py와 같은 폴더 안에 있는 models.py를 불러옴

# Register your models here.
# admin 패널을 바꿀 수 있음


@admin.register(models.User)  # decorator(class 위에 있어야 함) / admin 패널에서 user를 확인
class CustomUserAdmin(UserAdmin):

    """ Custom User Admin """

    fieldsets = UserAdmin.fieldsets + (
        (
            "Custom Profile",
            {
                "fields": (
                    "avatar",
                    "gender",
                    "bio",
                    "birthday",
                    "language",
                    "currency",
                    "superhost",
                )
            },
        ),
    )

    list_filter = UserAdmin.list_filter + ("superhost",)

    list_display = (
        "username",
        "first_name",
        "last_name",
        "email",
        "is_active",
        "language",
        "currency",
        "superhost",
        "is_staff",
        "is_superuser",
    )

    # list_display = ("username", "email", "gender", "language", "currency", "superhost") : user list에 보여질 것들
    # list_filter = ("language", "currency", "superhost") : 원하는 정보로 필터링 해서 볼 수 있음

    # fieldsets : admin 패널의 푸른색 구역(Personal info, Permissions, Important dates, Custom Profile)
    # UserAdmin.fieldsets : django에 있는 field

