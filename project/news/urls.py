from django.urls import path
from .views import PostList, PostDetail, PostSearchView

app_name = 'news'

urlpatterns = [
    path('', PostList.as_view(), name='post_list'),
    path('<int:pk>/', PostDetail.as_view(), name='post_detail'),
    path('search/', PostSearchView.as_view(), name='post_search'),
]