# Generated by Django 3.1.7 on 2021-03-16 16:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0003_publicaciones'),
    ]

    operations = [
        migrations.AddField(
            model_name='publicaciones',
            name='name_user',
            field=models.CharField(default='', max_length=140),
        ),
    ]
