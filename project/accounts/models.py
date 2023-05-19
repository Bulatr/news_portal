from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Author(models.Model):
    id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(User, related_name='users', on_delete=models.CASCADE)
    rating = models.CharField(max_length=255)
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(null=True, blank=True, default=None, auto_now=True)

    class Meta:
        db_table = "news_portal_author"

    def update_rating(self) -> None:
        pass
