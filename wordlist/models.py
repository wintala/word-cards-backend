from django.db import models

class Vocabulary(models.Model):
    name = models.CharField(max_length=50)

    @property
    def wordpairs(self):
        return self.wordpair_set.all()

class WordPair(models.Model):
    word = models.CharField(max_length=50)
    translation = models.CharField(max_length=50)
    vocabulary = models.ForeignKey(Vocabulary, on_delete=models.CASCADE)
