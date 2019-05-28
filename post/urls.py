from .views import PostCreate
from django.urls import path

app_name = 'post'

urlpatterns = [
    path('create/', PostCreate.as_view(), name='create')
]