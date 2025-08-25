from django.db import models

class Source(models.Model):
    name = models.TextField()

    def __str__(self):
        return self.name

class Quote(models.Model):
    quote_text = models.TextField()
    weight = models.IntegerField()
    source = models.ForeignKey(Source, on_delete=models.CASCADE)

    likes = models.IntegerField(default=0)
    dislikes = models.IntegerField(default=0)

    def __str__(self):
        return self.quote_text

class PageViews(models.Model):
    total_views = models.IntegerField(default=0)