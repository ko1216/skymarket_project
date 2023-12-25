from django.db import models

from users.models import User

NULLABLE = {'blank': True, 'null': True}


class Ad(models.Model):
    title = models.CharField(max_length=150, verbose_name='title', default='Some title')
    image = models.ImageField(upload_to='ads_images', verbose_name='image', **NULLABLE)
    price = models.DecimalField(max_digits=11, decimal_places=2, verbose_name='price', default=0.00)
    description = models.TextField(verbose_name='description', **NULLABLE)
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='author', **NULLABLE)
    created_at = models.DateTimeField(auto_now_add=True, **NULLABLE)
    updated_at = models.DateTimeField(auto_now=True, **NULLABLE)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Ad'
        verbose_name_plural = 'Ads'


class Comment(models.Model):
    text = models.TextField(verbose_name='text', default='new comment')
    author = models.ForeignKey(User, on_delete=models.PROTECT, verbose_name='author', **NULLABLE)
    ad = models.ForeignKey(Ad, on_delete=models.CASCADE, verbose_name='ad', **NULLABLE)
    created_at = models.DateTimeField(auto_now_add=True, **NULLABLE)

    def __str__(self):
        return f'{self.author}: {self.text[:10]}'

    class Meta:
        verbose_name = 'Comment'
        verbose_name_plural = 'Comments'
