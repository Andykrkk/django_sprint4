from django.urls import include, path

from . import views

app_name = 'blog'

posts_urls = [
    path('<int:post_id>/',
         views.PostDetailView.as_view(),
         name='post_detail'
         ),
    path('create/',
         views.PostCreateView.as_view(),
         name='create_post'
         ),

    path('<int:post_id>/edit/',
         views.PostUpdateView.as_view(),
         name='edit_post'
         ),

    path('<int:post_id>/delete/',
         views.PostDeleteView.as_view(),
         name='delete_post'
         ),

    path('<int:post_id>/comment/',
         views.CommentCreateView.as_view(),
         name='add_comment'
         ),

    path('<int:post_id>/edit_comment/<int:comment_id>',
         views.CommentUpdateView.as_view(),
         name='edit_comment'
         ),

    path('<int:post_id>/delete_comment/<int:comment_id>',
         views.CommentDeleteView.as_view(),
         name='delete_comment'
         )
]

urlpatterns = [
    path('', views.PostsHomepageView.as_view(), name='index'),
    path('posts/', include(posts_urls)),
    path(
        'edit_profile/', views.ProfileUpdateView.as_view(), name='edit_profile'
    ),
    path(
        'profile/<str:username>/',
        views.UserProfileDetailView.as_view(),
        name='profile',
    ),
    path(
        'category/<str:category_slug>/',
        views.CategoryDetailView.as_view(),
        name='category_posts',
    ),
]