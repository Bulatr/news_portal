from django.db import models
from accounts.models import Author

class Type(models.Model):

    article = 'ART'
    news = 'NEW'
    document = 'DOC'

    TYPE_POST = [
        (article, 'Статья'),
        (news, 'Новость'),
        (document, 'Документ')
    ]

    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=3, choices=TYPE_POST)
    slug = models.SlugField(null=True, blank=True, unique=True, error_messages={"unique": "Этот slug уже используется. Переименуйте заголовок или вручную укажите slug."})
    description = models.TextField(null=True)
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)

    class Meta:
        managed = False
        db_table = "news_portal_type"

    def save(self, *args, **kwargs):
        # Автоматическое создание слага на основе заголовка статьи
        self.slug = self.title.lower().replace(' ', '-')
        super().save(*args, **kwargs)


class Category(models.Model):
    id = models.AutoField(primary_key=True)
    category_name = models.TextField()
    slug = models.SlugField(null=True, blank=True, unique=True, error_messages={"unique": "Этот slug уже используется. Переименуйте заголовок или вручную укажите slug."})
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(null=True, blank=True, default=None, auto_now=True)

    class Meta:
        managed = False
        db_table = "news_portal_category"

    def save(self, *args, **kwargs):
        # Автоматическое создание слага на основе заголовка статьи
        self.slug = self.category_name.lower().replace(' ', '-')
        super().save(*args, **kwargs)


class Post(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.TextField(null=False, blank=False)

    # Используется для урл
    slug = models.SlugField(null=True, blank=True, unique=True, error_messages={"unique": "Этот slug уже используется. Переименуйте заголовок или вручную укажите slug."})
    content_data = models.TextField()

    # Пост может принадлежать только к одному типу
    type_id = models.ForeignKey(Type,related_name="types", on_delete=models.CASCADE)

    # Многие ко многим используя таблицу news_portal_post_category
    # category_id = models.ManyToManyField(Category, related_name='categoryes', through="news_portal_post_category", on_delete=models.CASCADE)

    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(null=True, blank=True, default=None, auto_now=True)

    # может принадлежать только к одному автору
    author_id = models.ForeignKey(Author, related_name="authors", on_delete=models.CASCADE)

    rating = models.IntegerField(null=True, blank=True)

    class Meta:
        managed = False
        db_table = "news_portal_category"

    def save(self, *args, **kwargs):
        # Автоматическое создание слага на основе заголовка статьи
        self.slug = self.title.lower().replace(' ', '-')
        super().save(*args, **kwargs)


# Класс промежуточной таблицы реализующей связь многие ко многим
class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('post', 'category')
        managed = False
        db_table = "news_portal_post_category"

class Comment(models.Model):
    id = models.AutoField(primary_key=True)
    text_comment = models.TextField(blank=False, null=False)
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(null=True, blank=True, default=None, auto_now=True)
    author_id = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField()

    # комментарий может быть прикреплен только к одному посту
    post_id = models.ForeignKey(Post, related_name='posts', on_delete=models.CASCADE)

    class Meta:
        managed = False
        db_table = "news_portal_comment"