from django.shortcuts import render
from .models import Post
from django.views.generic import CreateView, ListView, DetailView, DeleteView, UpdateView
# Create your views here.



class PostCreate(CreateView):
    model = Post
    template_name = 'post/create_post.html'
    success_url = 'post/detail_post.html'