# Generated by Django 3.2.3 on 2021-06-04 10:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('search', '0004_alter_page_author'),
    ]

    operations = [
        migrations.AlterField(
            model_name='page',
            name='link',
            field=models.URLField(),
        ),
    ]
