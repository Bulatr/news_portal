from django.db import models

class Type(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.TextField(null=False, blank=False)
    slug = models.SlugField(null=False, blank=False)
    description = models.TextField(null=True)
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        # Автоматическое создание слага на основе заголовка статьи
        self.slug = self.title.lower().replace(' ', '-')
        super().save(*args, **kwargs)


class Category(models.Model):
    id = models.AutoField(primary_key=True)
    category_name = models.TextField()
    slug = models.SlugField()
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(null=True, blank=True, default=None, auto_now=True)
    type_id = models.ForeignKey(Type, related_name='types', on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        # Автоматическое создание слага на основе заголовка статьи
        self.slug = self.category_name.lower().replace(' ', '-')
        super().save(*args, **kwargs)



