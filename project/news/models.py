from django.db import models
from django.contrib.auth.models import User

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
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        # Автоматическое создание слага на основе заголовка статьи
        self.slug = self.title.lower().replace(' ', '-')
        super().save(*args, **kwargs)


class Category(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(null=False, blank=False, max_length=255, unique=True)
    slug = models.SlugField(null=True, blank=True, unique=True, error_messages={"unique": "Этот slug уже используется. Переименуйте заголовок или вручную укажите slug."})
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)



    def save(self, *args, **kwargs):
        # Автоматическое создание слага на основе заголовка статьи
        self.slug = self.title.lower().replace(' ', '-')
        super().save(*args, **kwargs)


class Post(models.Model):
    from accounts.models import Author

    id = models.AutoField(primary_key=True)
    title = models.CharField(null=False, blank=False, max_length=255)

    # Используется для урл
    slug = models.SlugField(null=True, blank=True, unique=True, error_messages={"unique": "Этот slug уже используется. Переименуйте заголовок или вручную укажите slug."})
    content = models.TextField()

    # Пост может принадлежать только к одному типу
    # с помощию posts получим все посты с данным типом
    typepost = models.ForeignKey(Type,related_name="posts", on_delete=models.CASCADE)

    # Многие ко многим используя таблицу news_portal_post_category
    # category_id = models.ManyToManyField(Category, related_name='categoryes', through="news_portal_post_category", on_delete=models.CASCADE)

    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)

    # может принадлежать только к одному автору
    # через related_name="posts" можно получить все посты этого автора
    author = models.ForeignKey(Author, related_name="posts", on_delete=models.CASCADE)

    # пока реализовано простейшая схема голосования, без учета количества голосовавших
    rating = models.IntegerField(null=True, blank=True, default=0)

    # связь многие ко многим с категориями
    categories = models.ManyToManyField(Category)


    def save(self, *args, **kwargs):
        # Автоматическое создание слага на основе заголовка статьи
        self.slug = self.title.lower().replace(' ', '-')
        super().save(*args, **kwargs)

    def like(self) -> None:
        if self.rating < 10:
            self.rating += 1
            self.save()

    def dislike(self) -> None:
        if self.rating > 1:
            self.rating -= 1
            self.save()

    def preview(self):
        preview_length = 124  # Длина предварительного просмотра
        if len(self.content) <= preview_length:
            return self.content
        else:
            return self.content[:preview_length] + "..."



class Comment(models.Model):
    id = models.AutoField(primary_key=True)
    text_comment = models.TextField(blank=False, null=False)
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField(null=True, blank=True, default=0)

    # комментарий может быть прикреплен только к одному посту
    # через comments можно получить все комментарии этого поста
    # реализуем связь с моделью Post
    post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)



    def like(self) -> None:
        if self.rating < 10:
            self.rating += 1
            self.save()

    def dislike(self) -> None:
        if self.rating > 1:
            self.rating -= 1
            self.save()
