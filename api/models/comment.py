from django.db import models

from users.models import User

from .review import Review


class Comment(models.Model):
    text = models.TextField(verbose_name='Текст')
    review = models.ForeignKey(Review,
                               on_delete=models.CASCADE,
                               related_name='comments',
                               verbose_name='Отзыв')
    author = models.ForeignKey(User,
                               on_delete=models.CASCADE,
                               related_name='comments',
                               verbose_name='Автор')
    pub_date = models.DateTimeField(auto_now_add=True,
                                    verbose_name='Дата публикации',
                                    db_index=True)

    class Meta:
        ordering = ['-pub_date']

    def __str__(self):
        return self.pub_date, self.author
