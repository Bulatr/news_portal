from django.db import models
from django.contrib.auth.models import User
# from news.models import Post, Comment

# Create your models here.

class Author(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.OneToOneField(User, related_name='users', on_delete=models.CASCADE)
    rating = models.FloatField(blank=True, null=True, default=0.0 )
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)



    def get_posts(self):
        from news.models import Post
        return Post.objects.filter(author=self)

    def get_comments(self):
        from news.models import Comment
        return Comment.objects.filter(author=self)

    def update_rating(self):
        #author_posts = self.posts.all()
        #total_rating = sum(post.rating for post in author_posts)
        #total_rating = total_rating*3
        total_rating_posts = self.posts.aggregate(models.Sum('rating'))['rating__sum'] or 0
        total_rating_comments = self.posts.aggregate(models.Sum('rating'))['rating__sum'] or 0
        comments_rating = self.posts.annotate(comments_rating=models.Sum('comments__rating')).aggregate(models.Sum('comments_rating'))['comments_rating__sum'] or 0

        self.rating = ((total_rating_posts * 3) + comments_rating + total_rating_comments)/3
        self.save()

    # можно вызывать напрямую на классе Author, без создания экземпляра объекта этого класса.
    @classmethod
    def get_best_user(cls):
        # Используем order_by('-rating'), чтобы отсортировать авторов по убыванию рейтинга
        #  '-' перед полем 'rating' в методе order_by() указывает на сортировку по убыванию
        best_user = cls.objects.order_by('-rating').values('user__username', 'rating').first()
        if best_user:
            return best_user['user__username'], best_user['rating']
        else:
            return None, None