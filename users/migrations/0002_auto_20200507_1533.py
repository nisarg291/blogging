# Generated by Django 3.0.4 on 2020-05-07 10:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='mobile_no',
            field=models.TextField(default='', max_length=10),
        ),
    ]
