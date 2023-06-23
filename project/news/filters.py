import django_filters
from .models import Post

class PostFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(lookup_expr='icontains')
    published_date = django_filters.DateFilter()

    class Meta:
        model = Post
        fields = [
            'title',
            'create_time'
            ]