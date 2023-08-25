# Generated by Django 2.2.19 on 2023-08-05 12:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0004_auto_20230805_0005'),
    ]

    operations = [
        migrations.RenameField(
            model_name='post',
            old_name='pub_date',
            new_name='created',
        ),
        migrations.AlterField(
            model_name='comment',
            name='created',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Дата публикации'),
        ),
    ]