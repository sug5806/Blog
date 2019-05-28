from .views import PostCreate, PostList
from django.urls import path

app_name = 'post'

urlpatterns = [
    path('create/', PostCreate.as_view(), name='create'),
    path('', PostList.as_view(), name='list'),
]