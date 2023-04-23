# Generated by Django 4.1.5 on 2023-04-23 08:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_tags', '0011_alter_product_category'),
    ]

    operations = [
        migrations.CreateModel(
            name='Country',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(help_text='Китай', max_length=30, verbose_name='страна')),
            ],
            options={
                'verbose_name': 'страна производства',
                'verbose_name_plural': 'страны производства',
                'db_table': 'country',
            },
        ),
    ]
