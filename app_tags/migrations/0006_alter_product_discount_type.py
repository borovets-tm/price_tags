# Generated by Django 4.1.5 on 2023-02-04 11:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_tags', '0005_alter_product_is_red_price'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='discount_type',
            field=models.CharField(blank=True, choices=[('Акция !!!', 'Акция !!!'), ('Уценка', 'Уценка'), ('Витринный образец', 'Витринный образец'), ('Последний экземпляр', 'Последний экземпляр')], default='Акция !!!', max_length=100, null=True, verbose_name='причина скидки'),
        ),
    ]
