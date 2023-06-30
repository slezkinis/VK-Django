from django.db import models
from django.core.validators import MinValueValidator
from django.utils import timezone
from phonenumber_field.modelfields import PhoneNumberField

class ProductCategory(models.Model):
    title = models.CharField(
        'название',
        max_length=50
    )

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'категории'

    def __str__(self):
        return self.title


class Product(models.Model):
    title = models.CharField('Название', max_length=100)
    description = models.TextField('Описание')
    price = models.DecimalField(
        'цена',
        max_digits=8,
        decimal_places=2,
        validators=[MinValueValidator(0)]
    )
    image = models.ImageField(
        'картинка'
    )
    category = models.ForeignKey(
        ProductCategory,
        verbose_name='категория',
        related_name='products',
        null=True,
        blank=True,
        on_delete=models.CASCADE,
    )

    class Meta:
        verbose_name = 'товар'
        verbose_name_plural = 'товары'

    def __str__(self):
        return self.title


class Vk_user(models.Model):
    name = models.CharField('Имя пользователя', max_length=100, null=True)
    vk_id = models.IntegerField('ID пользователя')
    cart = models.CharField('Корзина для покупок', max_length=1000, null=True, blank=True)
    phonenumber = PhoneNumberField('Номер телефона клиента', blank=True, null=True)
    class Meta:
        verbose_name = 'пользователь'
        verbose_name_plural = 'пользователи'
    
    def __str__(self) -> str:
        return f'{self.name} {self.vk_id}'


class Order(models.Model):
    STATUSES = (
        ('payment', 'Проверка платежа'),
        ('first', 'Обработка'),
        ('second', 'Доставка'),
        ('third', 'Доставлен'),
        ('canceled', 'Отменён')
    )
    user = models.ForeignKey(
        Vk_user,
        verbose_name='Заказчик',
        related_name='orders',
        on_delete=models.CASCADE,
        null=True
    )
    address = models.CharField(
        verbose_name='Адрес',
        max_length=200,
        null=True,
        blank=True
    )
    status = models.CharField('Статус', choices=STATUSES, default='payment', max_length=100)
    comment = models.TextField('Комментарий', blank=True)
    created_at = models.DateTimeField('Время создания заказа', default=timezone.now)
    delivered_at = models.DateTimeField('Время доставки заказа', blank=True, null=True)

    class Meta:
        verbose_name = 'заказ'
        verbose_name_plural = 'заказы'
    
    def __str__(self) -> str:
        return f'{self.user.name} {self.created_at.date()}'


class OrderElements(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, verbose_name='Заказ', related_name='products')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Продукт', related_name='order_elements')
    quantity = models.IntegerField(verbose_name='Количество', validators=[MinValueValidator(1)])
    # price = models.DecimalField(verbose_name='Цена', max_digits=5, decimal_places=2, validators=[MinValueValidator(0)])
    price = models.FloatField('Цена', validators=[MinValueValidator(0)])
