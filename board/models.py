from django.db import models
from django.utils import timezone
from django.utils.timezone import now

from config import settings


class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    created_at = models.DateTimeField(default=now, editable=False)  # Добавляем поле

    def __str__(self):
        return self.name


class Advertisement(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(
        "Category",
        on_delete=models.SET_NULL,
        null=True,  # Разрешаем NULL
        blank=True,  # Разрешаем пустое значение в формах
    )
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="advertisements",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    image = models.ImageField(upload_to="ads_images/", null=True, blank=True)
    views = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.title


class Comment(models.Model):
    advertisement = models.ForeignKey(
        Advertisement, on_delete=models.CASCADE, related_name="comments"
    )
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    text = models.TextField(verbose_name="Текст отзыва")
    created_at = models.DateTimeField(default=timezone.now)
    rating = models.IntegerField(
        verbose_name="Оценка",
        help_text="Оцените объявление от 1 до 5",
        choices=[(i, str(i)) for i in range(1, 6)],
    )

    def __str__(self):
        return f"Comment by {self.owner} on {self.advertisement}"

    class Meta:
        verbose_name = "Отзыв"
        verbose_name_plural = "Отзывы"
        ordering = ["-created_at"]
