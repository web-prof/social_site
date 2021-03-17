from django.urls import path
from .views import *

app_name = 'posts'

urlpatterns = [
    path('', post_comment_create_list_view, name='main_post_view'),
    path('like_unlike/',like_unlike,name='like_unlike'),
    path('<pk>/delete/',post_delete_view.as_view(),name='post_delete_view'),
    path('<pk>/update/',post_update_view.as_view(),name='post_update_view'),
]
