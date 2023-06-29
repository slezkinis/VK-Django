# Generated by Django 4.2.2 on 2023-06-28 11:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('datacenter', '0009_alter_order_address'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('first', 'Обработка'), ('second', 'Доставка'), ('third', 'Доставлен'), ('canceled', 'Отменён')], default='first', max_length=100, verbose_name='Статус'),
        ),
    ]