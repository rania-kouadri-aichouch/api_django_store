from django.db import models
from django.conf import settings


# Create your models here.
class Comment(models.Model):
    user = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=False,
        blank=False
    )
    product = models.ForeignKey(
        to='products.Product',
        on_delete=models.CASCADE,
        null=False,
        blank=False
    )
    content = models.TextField(null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['created_at']
        verbose_name = 'Comment'
        verbose_name_plural = 'Comments'
        db_table = 'comments'

    def __str__(self):
        return '{}: {}'.format(self.user.username, self.content)


class Reply(models.Model):
    user = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=False,
        blank=False
    )
    comment = models.ForeignKey(
        to='comments_and_replies.Comment',
        on_delete=models.CASCADE,
        null=False,
        blank=False,
        related_name='replies'
    )
    content = models.TextField(null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['created_at']
        verbose_name = 'Reply'
        verbose_name_plural = 'Replies'
        db_table = 'replies'

    def __str__(self):
        return '{}: {}'.format(self.user.username, self.content)
