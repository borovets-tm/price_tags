# Generated by Django 4.1.5 on 2023-04-23 07:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app_tags', '0010_alter_category_title'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='category',
            field=models.ForeignKey(help_text='наушники', on_delete=django.db.models.deletion.CASCADE, to='app_tags.category', verbose_name='категория товара'),
        ),
    ]
