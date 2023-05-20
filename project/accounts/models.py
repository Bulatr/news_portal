from django.db import models
from django.contrib.auth.models import User
# from news.models import Post, Comment

# Create your models here.

class Author(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.OneToOneFieldAuthor(User, related_name='users', on_delete=models.CASCADE)
    rating = models.IntegerField()
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)



    def get_posts(self):
        from news.models import Post
        return Post.objects.filter(author=self)

    def get_comments(self):
        from news.models import Comment
        return Comment.objects.filter(author=self)

    def update_rating(self):
        posts = Author.get_posts()
        comments = Author.get_comments()
        articles_rating = posts.aggregate(models.Sum('rating'))['rating__sum'] or 0
        comments_rating = comments.aggregate(models.Sum('rating'))['rating__sum'] or 0
        article_comments_rating = posts.annotate(comments_rating=models.Sum('comments__rating')).aggregate(models.Sum('comments_rating'))['comments_rating__sum'] or 0

        self.rating = (articles_rating * 3) + comments_rating + article_comments_rating
        self.save()