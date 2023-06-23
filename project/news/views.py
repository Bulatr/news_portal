from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Post, Category
from .forms import SearchForm
from .filters import PostFilter

# Create your views here.
class PostList(ListView):
    # Указываем модель, объекты которой мы будем выводить
    model = Post
    # Поле, которое будет использоваться для сортировки объектов
    ordering = 'update_time'
    # Указываем имя шаблона, в котором будут все инструкции о том,
    # как именно пользователю должны быть показаны наши объекты
    template_name = 'post/post_list.html'
    # Это имя списка, в котором будут лежать все объекты.
    # Его надо указать, чтобы обратиться к списку объектов в html-шаблоне.
    context_object_name = 'posts'
    # пагинация
    paginate_by = 1

class PostDetail(DetailView):
    model = Post
    template_name = 'post/post_detail.html'
    context_object_name = 'post'

class PostSearchView(ListView):
    model = Post
    template_name = 'search_results.html'  # Укажите путь к вашему шаблону результатов поиска
    context_object_name = 'posts'

    def get_queryset(self):
        query = self.request.GET.get('q')
        if query:
            queryset = Post.objects.filter(title__icontains=query)
            return queryset
        return Post.objects.all()
