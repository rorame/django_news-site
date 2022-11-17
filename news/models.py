from django.db import models
from django.urls import reverse

# тут прописываем класс, который создает табличку в нашей базе данных
# атрибуты классса - отвечают за тип поля в нашей бд, какое поле будет создано на странице браузера, правила валидации

class News(models.Model):
    title = models.CharField(max_length=150)
    content = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Publication date')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Update date')
    photo = models.ImageField(upload_to='photos/%Y/%m/%d/', blank=True)
    is_published = models.BooleanField(default=True)
    category = models.ForeignKey('Category', on_delete=models.PROTECT, related_name='get_news')
    views = models.IntegerField(default=0)

    def get_absolute_url(self):
        return reverse('view_news', kwargs={"pk": self.pk})

    # волшебный метод, который возвращает название новости
    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "News"
        verbose_name_plural = "News"
        ordering = ['-created_at']


class Category(models.Model):
    title = models.CharField(max_length=150, db_index=True, verbose_name='Topic')

    def get_absolute_url(self):
        return reverse('category', kwargs={"category_id": self.pk})

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Topic"
        verbose_name_plural = "Topics"
        ordering = ['title']
