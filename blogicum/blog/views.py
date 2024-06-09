from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count
from django.http.response import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.urls import reverse, reverse_lazy
from django.utils import timezone
from django.views.generic import (
    CreateView, DeleteView, DetailView, ListView, UpdateView
)

from blog.models import Category, Comment, Post, User
from blog.mixins import CommentMixin, PostMixin, PostQuerySetMixin
from blog.forms import CommentForm, PostForm, ProfileForm


INDEX_POST_COUNT = 10


class Index(PostQuerySetMixin, ListView):
    """Главная страница"""

    paginate_by = INDEX_POST_COUNT
    template_name = 'blog/index.html'

    def get_queryset(self):
        return super().get_queryset().annotate(
            comment_count=Count('comments')).order_by('-pub_date')


class PostDetail(DetailView, PostMixin):
    """Страница отдельного поста"""

    model = Post
    template_name = 'blog/detail.html'
    success_url = reverse_lazy('blog:index')
    pk_url_kwarg = 'post_id'

    def get_object(self, queryset=None):
        return get_object_or_404(self.model, pk=self.kwargs[self.pk_url_kwarg])
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = CommentForm()
        context['comments'] = (
            self.object.comments.select_related(
                'author'
            ).order_by('created_at')
        )
        return context

    def get_success_url(self):
        return reverse(
            'blog:profile', kwargs={'username': self.object.author.username}
        )


class CategoryPosts(PostQuerySetMixin, ListView):
    """Страница отдельной категории."""

    template_name = 'blog/category.html'
    category = None
    paginate_by = INDEX_POST_COUNT




    def get_queryset(self):
        self.category = get_object_or_404(
            Category,
            slug=self.kwargs['category_slug'],
            is_published=True
        )
        return super().get_queryset().filter(
            is_published=True,
            category__is_published=True,
            pub_date__lte=timezone.now(),
            category__slug=self.kwargs['category_slug']
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = self.category
        return context


class ProfileList(PostQuerySetMixin, ListView):
    """Страница профиля пользователя"""

    model = Post
    template_name = 'blog/profile.html'
    paginate_by = INDEX_POST_COUNT

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profile'] = User.objects.get(username=self.kwargs['username'])
        return context
    
    def get_object(self, queryset=None):
        return get_object_or_404(self.model, pk=self.kwargs[self.pk_url_kwarg])

    def get_queryset(self):
        self.author = get_object_or_404(User, username=self.kwargs['username'])
        if self.request.user.username == self.kwargs['username']:
            return Post.objects.select_related(
                'location', 'category', 'author'
            ).filter(
                author=self.author
            ).order_by('-pub_date').annotate(
                comment_count=Count('comments')
            )

        return Post.objects.select_related(
            'location', 'category', 'author'
        ).filter(
            author=self.author,
            pub_date__lte=timezone.now(),
            is_published=True,
            category__is_published=True,
        ).order_by('-pub_date').annotate(comment_count=Count('comments'))


class ProfileUpdate(LoginRequiredMixin, UpdateView):
    """редактирование страницы профиля пользователя"""

    model = User
    form_class = ProfileForm
    template_name = 'blog/user.html'

    def get_object(self):
        return self.request.user

    def get_success_url(self):
        return reverse(
            'blog:profile',
            kwargs={'username': self.request.user.username},
        )


class PostCreate(LoginRequiredMixin, CreateView):
    """Страница создания поста"""

    model = Post
    template_name = 'blog/create.html'
    form_class = PostForm

    def get_success_url(self):
        username = self.request.user.username
        success_url = reverse(
            'blog:profile',
            kwargs={'username': username}
        )
        return success_url

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostUpdate(LoginRequiredMixin, PostMixin, UpdateView):
    """Редактирование поста"""

    def test_func(self):
        return self.get_object().author == self.request.user

    def handle_no_permission(self):
        post = self.get_object()
        return HttpResponseRedirect(reverse_lazy('blog:post_detail',
                                                 args=[post.pk]))

    def get_object(self, queryset=None):
        return get_object_or_404(self.model, pk=self.kwargs[self.pk_url_kwarg])

    def get_success_url(self):
        return reverse('blog:post_detail', args=[self.object.pk])


class PostDelete(LoginRequiredMixin, PostMixin, DeleteView):
    """Удаление поста"""

    def get_success_url(self):
        return reverse('blog:profile', args=[self.request.user.username])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = PostForm(instance=context['post'])
        return context


class CommentCreate(LoginRequiredMixin, CreateView):
    """Страница написания комментария"""

    model = Comment
    form_class = CommentForm
    posts = None
    pk_url_kwarg = 'post_id'

    def get_success_url(self):
        return reverse(
            'blog:post_detail', kwargs={'post_id': self.kwargs['post_id']}
        )

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.post = get_object_or_404(Post, pk=self.kwargs['post_id'])
        return super().form_valid(form)


class CommentUpdate(LoginRequiredMixin, CommentMixin, UpdateView,):
    """Редактирование коментария"""

    pass


class CommentDelete(LoginRequiredMixin, CommentMixin, DeleteView,):
    """Удаление коментария"""

    pass
