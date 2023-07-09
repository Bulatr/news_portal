from django.urls import path
from .views import PostList, PostDetail, PostSearchView, create_post, update_post, PostDelete

app_name = 'news'

urlpatterns = [
    path('', PostList.as_view(), name='post_list'),
    path('<int:pk>/', PostDetail.as_view(), name='post_detail'),
    path('search/', PostSearchView.as_view(), name='post_search'),
    path('create/', create_post, name='post_create'),
    path('<int:post_id>/update/', update_post, name='post_update'),
    path('<int:pk>/delete/', PostDelete.as_view(), name='post_delete'),
]