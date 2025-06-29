from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    ROLES = (
        ('user', 'Пользователь'),
        ('admin', 'Администратор'),
    )

    # Переопределяем username (не используется, вместо него email)
    username = None

    # Обязательные поля
    email = models.EmailField(unique=True, verbose_name='Email')
    phone = models.CharField(max_length=20, verbose_name='Телефон')
    first_name = models.CharField(max_length=50, verbose_name='Имя')
    last_name = models.CharField(max_length=50, verbose_name='Фамилия')
    role = models.CharField(max_length=10, choices=ROLES, default='user', verbose_name='Роль')
    image = models.ImageField(upload_to='photo/', blank=True, null=True, verbose_name='Аватар')
    token = models.CharField(max_length=100, verbose_name='Токен пользователя', blank=True, null=True)

    # Указываем, что email — поле для входа
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'phone']

    def __str__(self):
        return f'{self.first_name} {self.last_name} ({self.email})'

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
