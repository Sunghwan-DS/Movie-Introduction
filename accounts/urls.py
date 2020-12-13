from django.urls import path
from . import views
app_name='accounts'

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('<int:pk>/detail/', views.user_detail, name = 'detail'),
    path('<int:pk>/detail/update/', views.user_update, name = 'update'),
    path('<int:pk>/follow/', views.follow, name='follow'),
    path('delete/', views.delete, name='delete'),
]