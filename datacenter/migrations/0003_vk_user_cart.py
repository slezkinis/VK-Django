# Generated by Django 4.2.2 on 2023-06-26 13:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('datacenter', '0002_vk_user_remove_order_firstname_remove_order_lastname_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='vk_user',
            name='cart',
            field=models.CharField(default='', max_length=1000, verbose_name='Корзина для покупок'),
        ),
    ]