from django.shortcuts import render
from django.http import JsonResponse

from .models import Post
from django.views.generic import CreateView, ListView, DetailView, DeleteView, UpdateView, View
from django.shortcuts import redirect, get_list_or_404, get_object_or_404
from django.urls import reverse_lazy

# 제네릭 뷰를 사용해서 클래스형 뷰를 만들때는 상속을 한다
# 함수형 뷰처럼 모든 내용을 직접 구현하고 싶을 때는 View를 상속 받는다 ex) API View

# Create your views here.

"""
응답시간의 병목
1. DB
2. Template 렌더링 
"""



# 일반적인 뷰
class IndexView(View):
    def get(self, *args, **kwargs):
        return render(self.request, 'post/list_post.html')

def indexView(request):
    if request.method == "GET":
        return render(request, 'post/list_post.html')

#######################################################################

class JsonView(View):
    def get(self, *args, **kwargs):
        return JsonResponse({"data": 'test'})

def jsonView(request):
    if request.method == "GET":
        return JsonResponse({"data": 'test'})


########################################################################

def apiView(request):
    if request.method == "POST":
        pass
    else:
        pass




########################################################################

from django.contrib.auth.mixins import LoginRequiredMixin

# Create

### CBV
class PostCreate(LoginRequiredMixin, CreateView):
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

    """
    이렇게도 가능 
    def form_valid(self, form):
        form.instance.author_id = self.request.user.id
        return super().form_valid(form)
        
    """


### FBV

from django.forms.models import modelform_factory

def postCreate(request):
    # from_factory : 폼을 쉽게 생성하기 위해 사용하는 클래스, Factory 패턴
    # 기존에 Form Class를 별도로 만드는 방식보다 간단하게 폼을 만들어서 처리할 수 있다는 장점이 있다.
    form_class = modelform_factory(Post, fields=['category', 'title', 'text'])
    if request.method == "POST":
        # 입력이 완료 되었을떄
        form = form_class(request.POST)
        # 작성자 ID를 입력받는 곳이 없어서 해줌
        form.instance.author_id = request.user.id
        if form.is_valid():
            instance = form.save()
            return redirect(instance)
    else:
        # 입력 폼 출력
        form = form_class()
        pass

    return render(request, 'post/create_post.html', {'form': form})

################################################################################

# List

### CBV
class PostList(ListView):
    model = Post
    template_name = 'post/list_post.html'
    paginate_by = 1

    def post(self, *args, **kwargs):
        queryset = Post.objects.all()
        search_key = self.request.POST.get('search_key', None)
        cb_key = self.request.POST.get('search_type', None)
        print(cb_key)
        print(search_key)
        if search_key:
            queryset = queryset.filter(text__icontains=search_key)

    def get_context_data(self, *, object_list=None, **kwargs):
        pass

    """
    setup()
    dispatch()
    get_object()
    get_queryset()
    get_context_data()
    render_to_response()
    """

### FBV

from django.core.paginator import Paginator
from django.db.models import Q

def postList(request):




    # 검색기능
    queryset = Post.objects.all()
    search_keyword = request.POST.get('search', request.GET.get('search', None))
    context_data = {}

    if search_keyword:
        q = Q(text__icontains = search_keyword)
        q |= Q(title__icontains = search_keyword)
        queryset = queryset.filter(q)
        context_data.update({'earch_keyword': search_keyword})

    # 페이지 번호 얻기
    page = int(request.GET.get('page', 1))
    object_list = Post.objects.all()  # CBV : get_queryset이 해준다

    # 페이징 처리
    paginator = Paginator(queryset, 1)
    page = paginator.page(page)
    context_data.update({
                         'object_list': page.object_list,
                         'paginator': paginator,
                         'page_obj': page,
                         'is_paginated': True,
                         })


    return render(request, 'post/list_post.html', {context_data})

################################################################

# Detail

### CBV
class PostDetail(DetailView):
    model = Post
    template_name = 'post/detail_post.html'


### FBV

from django.http import Http404

def postDetail(request, pk):
    try:
        object = Post.objects.get(pk=pk)
    except:
        raise Http404("Post does not exists")
    return render(request, 'blog/post_detail.html', {'object': object})


###################################################################

# Update
### CBV
class PostUpdate(UpdateView):
    model = Post
    fields = ['category', 'title', 'text']
    template_name = 'post/update_post.html'
    success_url = reverse_lazy('post:list')  # , args=)

    # form_vaild를 안해준 이유는 ID값을 변경할 이유가 없어서임

    # pk_url_kwarg = 원하는 이름
    # success_url = 'detail/{pk}/'
    # success_url이 있는 Create, Update, Delete의 경우
    # 클래스의 속성값을 사용해서 URL을 만들 수 있다.
    # success_url = 'pattern/{변수명}/'

    """
    setup()
    dispatch()
    
    get()
    post() - 저장처리
    
    get_object()
    
    get_context_data()
    render_to_response()
    """



### FBV

def postUpdate(request, pk):
    object = get_object_or_404(Post, pk=pk)
    # from_factory : 폼을 쉽게 생성하기 위해 사용하는 클래스, Factory 패턴
    # 기존에 Form Class를 별도로 만드는 방식보다 간단하게 폼을 만들어서 처리할 수 있다는 장점이 있다.
    form_class = modelform_factory(Post, fields=['category', 'title', 'text'])
    if request.method == "POST":
        # 입력이 완료 되었을떄
        # 수정시에는 instance 저장 필수
        form = form_class(request.POST, instance=object)
        if form.is_valid():
            instance = form.save()
            return redirect(instance)

    else:
        form = form_class(instance=object)
    return render(request, 'post/update_post.html', {'form': form})




##################################################################

# Delete

### CBV

class PostDelete(DeleteView):
    model = Post
    template_name = 'post/delete_post.html'
    success_url = reverse_lazy('post:list')




### FBV

def postDelete(request, pk):
    object = get_object_or_404(Post, pk=pk)

    if request.method == "POST":
        object.delete()
        redirect('post:list')
    else:
        return render(request, 'post/delete_post.html')
