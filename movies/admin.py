from django.contrib import admin
from .models import Review, Movie, Genre, RepNationNm
# Register your models here.

class GenreAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')

class RepNationNmAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')

class ReviewAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'content', 'created_at', 'updated_at', )

class MovieAdmin(admin.ModelAdmin):
    list_display = ('movieNm', 'poster_path')


# 어드민 사이트에 등록해줘
admin.site.register(Review, ReviewAdmin)
admin.site.register(Movie, MovieAdmin)
admin.site.register(Genre, GenreAdmin)
admin.site.register(RepNationNm, RepNationNmAdmin)