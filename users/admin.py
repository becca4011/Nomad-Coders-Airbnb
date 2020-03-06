from django.contrib import admin
from . import models  # admin.py와 같은 폴더 안에 있는 models.py를 불러옴

# Register your models here.


@admin.register(models.User)
class CustomUserAdmin(admin.ModelAdmin):
    pass
