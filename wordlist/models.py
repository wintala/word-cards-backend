from django.contrib.auth.models import User
from django.db import models


class Vocabulary(models.Model):
    name = models.CharField(max_length=50)
    owner = models.ForeignKey(User, verbose_name = 'User', on_delete=models.SET_NULL, null=True)

    @property
    def wordpairs(self):
        return self.wordpair_set.all()

class WordPair(models.Model):
    word = models.CharField(max_length=50)
    translation = models.CharField(max_length=50)
    vocabulary = models.ForeignKey(Vocabulary, on_delete=models.CASCADE)
