# Generated by Django 4.1.7 on 2023-03-07 16:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0010_post_slug'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='recommended',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='post',
            name='top_pick',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='post',
            name='featured',
            field=models.BooleanField(default=False),
        ),
    ]