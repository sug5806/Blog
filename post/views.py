from django.shortcuts import render
from .models import Post
from django.views.generic import CreateView, ListView, DetailView, DeleteView, UpdateView
from django.shortcuts import redirect, get_list_or_404, get_object_or_404
from django.urls import reverse_lazy
import math

# Create your views here.



class PostCreate(CreateView):
    model = Post
    fields = ['category', 'title', 'text']
    template_name = 'post/create_post.html'
    success_url = 'post/detail_post.html'


    def form_valid(self, form):
        # 입력된 자료가 올바른지 채크
        form.instance.author_id = self.request.user.id
        if form.is_valid():
            # 올바르다면
            # form : 모델 폼
            form.instance.save()
            return redirect('/')
        else:
            # 올바르지 않다면
            return self.render_to_response({'form': form})



class PostList(ListView):
    model = Post
    template_name = 'post/list_post.html'
    paginate_by = 1


class PostDetail(DetailView):
    model = Post
    template_name = 'post/detail_post.html'


class PostUpdate(UpdateView):
    model = Post
    fields = ['category', 'title', 'text']
    template_name = 'post/update_post.html'
    success_url = reverse_lazy('post:detail')


class PostDelete(DeleteView):
    model = Post
    template_name = 'post/delete_post.html'
    success_url = '/'
