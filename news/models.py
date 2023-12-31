from django.db import models
from django.contrib.auth.models import User


class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    rating = models.IntegerField(default=0)

    def update_rating(self):
        self.rating = 0
        for post in self.post_set.all():
            self.rating += post.rating * 3
            for comment in post.comment_set.all():
                self.rating += comment.rating
        for comment in self.comment_set.all():
            self.rating += comment.rating
        self.save()


class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)

class PostCategory(models.Model):
    post = models.ForeignKey('Post', on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

class Post(models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE)

    ARTICLE = 'AR'
    NEWS = 'NE'

    POST_TYPE_CHOICES= [
        (ARTICLE, 'Статья'),
        (NEWS, 'Новость'),
    ]

    post_type = models.CharField(max_length=2, choices=POST_TYPE_CHOICES, default=ARTICLE,)
    created_at = models.DateTimeField(auto_now_add=True)
    category = models.ManyToManyField(Category, through= 'PostCategory')
    title = models.CharField(max_length=200)
    text = models.TextField()
    rating = models.IntegerField(default=0)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    def preview(self):
        if len(self.content) > 124:
            return self.content[:124] + "..."
        else:
            return self.content


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    rating = models.IntegerField(default=0)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

