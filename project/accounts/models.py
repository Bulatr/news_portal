from django.db import models
from django.contrib.auth.models import User
# from news.models import Post, Comment

# Create your models here.

class Author(models.Model):
    id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(User, related_name='users', on_delete=models.CASCADE)
    rating = models.IntegerField()
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(null=True, blank=True, default=None, auto_now=True)

    class Meta:
        managed = False
        db_table = "news_portal_author"

    def update_rating(self):
        posts = self.posts.all()
        comments = self.comments.all()
        articles_rating = posts.aggregate(models.Sum('rating'))['rating__sum'] or 0
        comments_rating = comments.aggregate(models.Sum('rating'))['rating__sum'] or 0
        article_comments_rating = self.posts.annotate(comments_rating=models.Sum('comments__rating')).aggregate(models.Sum('comments_rating'))['comments_rating__sum'] or 0

        self.rating = (articles_rating * 3) + comments_rating + article_comments_rating
        self.save()