# Generated by Django 4.0.5 on 2022-07-31 09:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myfirsttry', '0014_rename_reviewer_comment_testcase_comment_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='testcase_title',
            name='tc_author',
        ),
        migrations.DeleteModel(
            name='TestCase',
        ),
        migrations.DeleteModel(
            name='TestCase_Title',
        ),
    ]
