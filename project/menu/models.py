from django.db import models

# Create your models here.
class Menu(models.Model):
    MENU_CHOICES = (
        ('main', 'Основное меню'),
        ('top', 'Верхнее меню')
    )
    menu_name = models.CharField(max_length=50, choices=MENU_CHOICES, default='main')
    name = models.CharField(max_length=255)
    url = models.CharField(max_length=255)
    order = models.IntegerField(default=0)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['order']