from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView
from .models import Post, Category
from .forms import SearchForm, PostForm
from .filters import PostFilter
from django.utils import timezone
from datetime import datetime
from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView, DeleteView
)
from django.urls import reverse_lazy

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
    
# Обработка данных формы
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save()
            post_id = post.id
            # Дополнительные действия после сохранения формы
            return redirect('post/post_detail', post_id=post_id)
    else:
        form = PostForm()
    return render(request, 'post/post_create.html', {'form': form})

def update_post(request, post_id):
    post = Post.objects.get(id=post_id)
    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            # после сохранения перенапрвляется на страницу товара
            return redirect('post/post_detail', post_id=post_id)
            # Дополнительные действия после сохранения формы
    else:
        form = PostForm(instance=post)
    return render(request, 'post/post_update.html', {'form': form})

class PostDelete(DeleteView):
    model = Post
    template_name = 'post/post_delete.html'
    success_url = reverse_lazy('post/post_list')