from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse

# Create your models here.
User = get_user_model()

class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = models.ImageField()


class Category(models.Model):
    title = models.CharField(max_length=20)
    slug = models.SlugField()

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = "Categories"




class Post(models.Model):
    title = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, default="undefined")
    overview = models.TextField(default='')
    content = models.TextField(default="<h1>No Content Available</h1>")
    timestamp = models.DateTimeField(auto_now_add=True)
    read_length = models.IntegerField(default=5)
    comment_count = models.IntegerField(default=0)
    view_count = models.IntegerField(default=0)
    author = models.ForeignKey(Author, on_delete=models.CASCADE, blank=True, null=True)
    thumbnail = models.ImageField(default='static_in_env/img/blog-post-1.jpeg')
    categories = models.ManyToManyField(Category, related_name='categories')
    primary_category = models.ForeignKey(Category, on_delete=models.SET_NULL, blank=True, null=True, related_name='primary_category')
    featured = models.BooleanField(default=False)
    top_pick = models.BooleanField(default=False)
    recommended = models.BooleanField(default=False)
    previous_post = models.ForeignKey('self', related_name='previous', on_delete=models.SET_NULL, blank=True, null=True)
    next_post = models.ForeignKey('self', related_name='next', on_delete=models.SET_NULL, blank=True,
                                      null=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post-detail', kwargs={
            'id': self.id
        })

    def get_absolute_url_slug(self):
        return reverse('post-detail', kwargs={
            'slug': self.slug
        })



