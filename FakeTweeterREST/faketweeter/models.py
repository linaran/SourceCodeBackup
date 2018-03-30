from django.db import models
from django.contrib.auth.models import User


class Tweet(models.Model):
    user = models.ForeignKey('auth.User', related_name='tweets', on_delete=models.CASCADE)
    tweet = models.CharField(max_length=200)
    date_published = models.DateTimeField('date published')

    def __str__(self):
        return str(self.tweet) + " " + str(self.date_published)
