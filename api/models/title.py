from datetime import datetime

from django.core.validators import MaxValueValidator
from django.db import models

from .category import Category
from .genre import Genre


class Title(models.Model):
    name = models.CharField(max_length=300,
                            verbose_name='name')
    year = models.IntegerField(null=True,
                               blank=True,
                               verbose_name='year',
                               validators=[MaxValueValidator(
                                   datetime.now().year,
                                   message='Is your title from the future?'
                               )])
    description = models.CharField(max_length=1000,
                                   blank=True,
                                   verbose_name='description')
    genre = models.ManyToManyField(Genre,
                                   related_name='titles',
                                   verbose_name='genre')
    category = models.ForeignKey(Category,
                                 on_delete=models.SET_NULL,
                                 blank=True,
                                 null=True,
                                 related_name='titles',
                                 verbose_name='category')

    class Meta:
        ordering = ['name']
