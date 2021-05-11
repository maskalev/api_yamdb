from django.db import models


class Genre(models.Model):
    name = models.CharField(max_length=30, verbose_name='genre')
    slug = models.SlugField(unique=True, verbose_name='slug')

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name
