from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from users.models import User

from .title import Title


class Review(models.Model):
    text = models.TextField()
    score = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)],
        verbose_name='Оценка',
    )
    title = models.ForeignKey(Title,
                              on_delete=models.CASCADE,
                              related_name='reviews',
                              blank=True,
                              verbose_name='Название произведения')
    author = models.ForeignKey(User,
                               on_delete=models.CASCADE,
                               related_name='reviews',
                               verbose_name='Автор')
    pub_date = models.DateTimeField(auto_now_add=True,
                                    verbose_name='Дата публикации',
                                    db_index=True)

    class Meta:
        ordering = ['-pub_date']

    def __str__(self):
        return f'{self.pub_date}, {self.author}, {self.title}'
