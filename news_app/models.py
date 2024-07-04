from django.db import models
from django.urls import reverse
from django.utils import timezone
from .managers import PublishedManager
from django.contrib.auth.models import User

class Cotegory(models.Model):
    name = models.CharField(max_length=150)

    def __str__(self):
        return self.name


class News(models.Model):
    
    class Status(models.TextChoices):
        Draft = 'DF', 'Draft'
        Published = 'PB', 'Published'

    title = models.CharField(max_length=150)
    slug = models.SlugField(max_length=150)
    body = models.TextField()
    image = models.ImageField(upload_to='media/')
    cotegory = models.ForeignKey(Cotegory, on_delete=models.CASCADE)
    publish_time = models.DateTimeField(default=timezone.now)
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=2, choices=Status.choices, default=Status.Draft)
    

    objects = models.Manager()
    published = PublishedManager()

    class Meta:
        ordering = ['-publish_time']


    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('detail_page', args=[self.slug])

class Cantact(models.Model):
    name = models.CharField(max_length=150)
    email = models.EmailField(max_length=150)
    message = models.TextField()

    def __str__(self):
        return self.email
    


class Comment(models.Model):
    news = models.ForeignKey(News, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    body = models.TextField()
    created_time = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)


    class Meta:
        ordering = ['created_time']

    def __str__(self):
        return f'{self.body} by {self.user}'
    