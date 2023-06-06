from django.urls import path
from .views import PostList, PostDetail

app_name = 'news'

urlpatterns = [
    path('', PostList.as_view(), name='product_list'),
    path('<int:pk>/', PostDetail.as_view(), name='product_detail'),
]