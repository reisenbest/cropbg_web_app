# Generated by Django 4.2.1 on 2023-06-12 06:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crop', '0004_alter_data_result_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='data',
            name='bgcolor',
            field=models.CharField(default=None, max_length=15, verbose_name='Цвет фона'),
        ),
    ]