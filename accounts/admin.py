from django.contrib import admin
from .models import User
# Register your models here.

class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'nickname', 'sex', 'age')


# 어드민 사이트에 등록해줘
admin.site.register(User, UserAdmin)