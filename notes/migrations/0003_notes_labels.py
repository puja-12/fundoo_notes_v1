# Generated by Django 4.1 on 2022-09-22 14:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('labels', '0001_initial'),
        ('notes', '0002_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='notes',
            name='labels',
            field=models.ManyToManyField(to='labels.labels'),
        ),
    ]
