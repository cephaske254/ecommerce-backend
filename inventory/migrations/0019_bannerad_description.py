# Generated by Django 3.1.4 on 2021-01-27 08:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0018_auto_20210125_1050'),
    ]

    operations = [
        migrations.AddField(
            model_name='bannerad',
            name='description',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]
