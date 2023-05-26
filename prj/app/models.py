from django.contrib.auth.models import User
from django.db import models
from django.db.models import Sum
from django.urls import reverse


class Author(models.Model):
    author_user = models.OneToOneField(User, on_delete=models.CASCADE)
    author_rating = models.SmallIntegerField(default=0)

    class Meta:
        verbose_name = 'Автор'
        verbose_name_plural = 'Авторы'

    def update_rating(self):
        post_rat = self.post_set.aggregate(post_rat=Sum('post_rating'))
        p_rat = 0
        p_rat += post_rat.get('post_rat')

        comment_rat = self.author_user.comment_set.aggregate(comment_rat=Sum('comment_rating'))
        c_rat = 0
        c_rat += comment_rat.get('comment_rat')

        self.author_rating = p_rat * 3 + c_rat
        self.save()


class Category(models.Model):
    name = models.CharField(max_length=64, unique=True, verbose_name='Категория')

    def __str__(self):
        return self.name


class Post(models.Model):
    NEWS = 'NW'
    ARTICLE = 'AR'
    CATEGORY_CHOICES = ((NEWS, 'Новость'), (ARTICLE, 'Статья'))
    type_category = models.CharField(max_length=2, choices=CATEGORY_CHOICES, default=ARTICLE,
                                     verbose_name='Тип категории')

    post_title = models.CharField('Заголовок', max_length=128)
    post_text = models.TextField('Текст', max_length=2048)
    post_author = models.ForeignKey(Author, on_delete=models.CASCADE)
    post_category = models.ManyToManyField(Category, through='PostCategory', verbose_name='Категория')
    post_rating = models.SmallIntegerField(default=0)
    post_date = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    post_date_update = models.DateTimeField(auto_now=True, verbose_name='Дата изменения')
    post_photo = models.ImageField(upload_to="photos/%Y/%m/%d/", blank=True)

    def __str__(self):
        return self.post_title


    class Meta:
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'
        ordering = ['-post_date', 'post_title']

    def preview(self):
        return self.post_text[0:350] + '...'

    def like(self):
        self.post_rating += 1
        self.save()

    def dislike(self):
        self.post_rating -= 1
        self.save()

    def get_absolute_url(self):
        return reverse('post', kwargs={'post_id': self.pk})


class PostCategory(models.Model):
    post_through = models.ForeignKey(Post, on_delete=models.CASCADE)
    category_through = models.ForeignKey(Category, on_delete=models.CASCADE)


class Comment(models.Model):
    comment = models.ForeignKey(Post, on_delete=models.CASCADE)
    comment_author = models.ForeignKey(User, on_delete=models.CASCADE)
    comment_text = models.TextField('Текст комментария', max_length=512)
    comment_date = models.DateTimeField('Дата комментария', auto_now=True)
    comment_rating = models.SmallIntegerField(default=0)

    def __str__(self):
        return self.comment_text

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    def like(self):
        self.comment_rating += 1
        self.save()

    def dislike(self):
        self.comment_rating -= 1
        self.save()
