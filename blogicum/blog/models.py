from django.db import models
from django.contrib.auth import get_user_model

from core.models import PublishedModel


User = get_user_model()

MAXIMUM_LENGTH_STRING = 256
STR_VIEWS_LENGTH = 20
COMMENTS_VIEWS_LIMIT = 10
SLUG_LENGTH = 64


class Location(PublishedModel):
    """Местоположение"""

    name = models.CharField(
        max_length=MAXIMUM_LENGTH_STRING,
        verbose_name='Название места'
    )

    class Meta:
        verbose_name = 'местоположение'
        verbose_name_plural = 'Местоположения'

    def __str__(self) -> str:
        return self.name[:STR_VIEWS_LENGTH]


class Category(PublishedModel):
    """Категория"""

    title = models.CharField(
        max_length=MAXIMUM_LENGTH_STRING,
        verbose_name='Заголовок'
    )
    description = models.TextField(verbose_name='Описание')
    slug = models.SlugField(
        max_length=SLUG_LENGTH,
        unique=True,
        verbose_name='Идентификатор',
        help_text='Идентификатор страницы для URL; '
                  'разрешены символы латиницы, цифры, дефис и подчёркивание.'
    )

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'Категории'

    def __str__(self) -> str:
        return self.title[:STR_VIEWS_LENGTH]


class Post(PublishedModel):

    title = models.CharField(
        max_length=MAXIMUM_LENGTH_STRING,
        verbose_name='Заголовок')
    text = models.TextField(verbose_name='Текст')
    pub_date = models.DateTimeField(
        verbose_name='Дата и время публикации',
        help_text='Если установить дату и время в будущем — '
                  'можно делать отложенные публикации.'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор публикации',
        related_name='posts'
    )
    location = models.ForeignKey(
        Location,
        on_delete=models.SET_NULL,
        verbose_name='Местоположение',
        related_name='posts',
        null=True,
        blank=True
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='Категория',
        related_name='posts'
    )
    image = models.ImageField(
        'Изображение',
        upload_to='post_images',
        blank=True,
    )

    class Meta:
        verbose_name = 'публикация'
        verbose_name_plural = 'Публикации'
        ordering = ['-pub_date', ]

    def __str__(self) -> str:
        return self.title[:STR_VIEWS_LENGTH]


class Comment(PublishedModel):
    text = models.TextField(
        verbose_name='Текст'
    )
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        verbose_name='Пост'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор'
    )

    class Meta:
        verbose_name = 'коментарий'
        verbose_name_plural = 'Коментарии'
        default_related_name = 'comments'
        ordering = ('created_at',)

    def __str__(self) -> str:
        return (f'Комментарий {self.author} к посту "{self.post}", '
                f'текст: {self.text[:COMMENTS_VIEWS_LIMIT]}')
