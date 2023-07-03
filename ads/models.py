from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=40, verbose_name='название')

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name

class Location(models.Model):
    name = models.CharField(max_length=40, verbose_name='название')
    lat = models.FloatField(verbose_name='широта', blank=True, null=True)
    lng = models.FloatField(verbose_name='долгота', blank=True, null=True)

    class Meta:
        verbose_name = 'Местоположение'
        verbose_name_plural = 'Местоположения'

    def __str__(self):
        return self.name


class User(models.Model):
    ROLES = [
        ("user", "Пользователь"),
        ("moderator", "Модератор"),
        ("admin", "Админ"),
        ("member", "Член сообщества")
    ]

    first_name = models.CharField(max_length=40, verbose_name='имя')
    last_name = models.CharField(max_length=40, verbose_name='фамилия')
    username = models.CharField(max_length=40, verbose_name='имя пользователя')
    password = models.CharField(max_length=40, verbose_name='пароль')
    role = models.CharField(max_length=10, choices=ROLES, default="user", verbose_name='роль')
    age = models.SmallIntegerField(verbose_name='возраст')
    locations = models.ManyToManyField(Location)

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.first_name


class Ad(models.Model):
    name = models.CharField(max_length=101, verbose_name='название')
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    price = models.PositiveIntegerField(verbose_name='цена')
    description = models.TextField(max_length=5000, verbose_name='описание')
    is_published = models.BooleanField(verbose_name='опубликовано')
    image = models.ImageField(upload_to="images/", verbose_name='фото')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)

    class Meta:
        verbose_name = 'Объявление'
        verbose_name_plural = 'Объявления'

    def __str__(self):
        return self.name
