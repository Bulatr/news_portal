from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Post, Category
from .forms import SearchForm
from .filters import PostFilter
from django.utils import timezone
from datetime import datetime

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
        queryset = super().get_queryset()
        query = self.request.GET.get('q')
        category_id = self.request.GET.get('category')
        date = self.request.GET.get('date')
        if query:
            # queryset = Post.objects.filter(title__icontains=query)
            queryset = queryset.filter(title__icontains=query)
        if category_id:
            queryset = queryset.filter(category=category_id)
        if date:
            start_date = timezone.make_aware(datetime.strptime(date, '%Y-%m-%dT%H:%M'))
            end_date = start_date.replace(hour=23, minute=59, second=59)
            queryset = queryset.filter(create_time__range=(start_date, end_date))
        return queryset

    # Чтобы вывести список всех категорий в форме, нужно передать список категорий из представления
    # в контекст шаблона. Затем вы можете использовать этот список в шаблоне для создания элементов
    # <option> в выпадающем списке

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context
