# Generated by Django 3.0.5 on 2020-05-07 08:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_registered'),
    ]

    operations = [
        migrations.AddField(
            model_name='registered',
            name='Cart',
            field=models.ManyToManyField(blank=True, to='users.Cart'),
        ),
    ]
