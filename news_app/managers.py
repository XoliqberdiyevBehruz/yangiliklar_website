from django.db import models
import news_app


class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status=news_app.models.News.Status.Published)