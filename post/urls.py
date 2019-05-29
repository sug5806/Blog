from .views import *
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path

app_name = 'post'

urlpatterns = [
    path('create/', PostCreate.as_view(), name='create'),
    path('detail/<int:pk>/', PostDetail.as_view(), name='detail'),
    path('update/<int:pk>/', PostUpdate.as_view(), name='update'),
    path('delete/<int:pk>/', PostDelete.as_view(), name='delete'),
    path('', PostList.as_view(), name='list'),
    path('login/', LoginView.as_view(template_name='account/login.html'), name='login'),
    path('logout/', LogoutView.as_view(template_name='account/logout.html'), name='logout'),
]