from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=30, verbose_name='category')
    slug = models.SlugField(unique=True, verbose_name='slug')

    class Meta:
        ordering = ['name']
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name
