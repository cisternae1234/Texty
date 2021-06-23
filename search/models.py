from django.db import models


class Page(models.Model):
    website = models.CharField(max_length=50)
    link = models.URLField()
    title = models.CharField(max_length=100)
    author = models.CharField(max_length=50, blank=True, null=True, default='')
    content = models.TextField()
    time = models.DateTimeField(blank=True, null=True, default=None)

    def __str__(self):
        return self.title
