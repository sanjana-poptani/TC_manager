# Generated by Django 4.0.5 on 2022-07-19 18:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myfirsttry', '0005_card'),
    ]

    operations = [
        migrations.AddField(
            model_name='card',
            name='release_num_word',
            field=models.CharField(default='zero', max_length=50),
            preserve_default=False,
        ),
    ]
