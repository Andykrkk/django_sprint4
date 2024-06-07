from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static

from . import views

app_name = 'blog'

posts = [
    path('<int:post_id>/', views.post_detail, name='post_detail'),
    path('create/', views.post_create,
         name='create_post'),
    path('<int:post_id>/edit/',
         views.post_update_view,
         name='edit_post'),
    path('<int:post_id>/delete/',
         views.post_delete, name='delete_post'),
    path('<int:post_id>/comment/', views.add_comment,
         name='add_comment'),
    path('<int:post_id>/edit_comment/<int:comment_id>/',
         views.edit_comment, name='edit_comment'),
    path('<int:post_id>/delete_comment/<int:comment_id>/',
         views.delete_comment, name='delete_comment')
]
profile = [
    path('<str:username>/', views.user_profile,
         name='profile'),
    path('edit/', views.profile_edit,
         name='edit_profile'),
]

urlpatterns = [
    path('', views.index, name='index'),
    path('category/<slug:category_slug>/',
         views.category_posts, name='category_posts'),
    path('posts/', include(posts)),
    path('profile/', include(profile)),
]
