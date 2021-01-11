# Generated by Django 3.1.4 on 2021-01-07 15:00

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0003_auto_20210107_1450'),
    ]

    operations = [
        migrations.RenameField(
            model_name='product',
            old_name='old_price',
            new_name='price',
        ),
        migrations.AlterField(
            model_name='product',
            name='discount_price',
            field=models.FloatField(blank=True, default='', max_length=200, null=True),
        ),
        migrations.CreateModel(
            name='deal',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start', models.DateTimeField(blank=True, default=datetime.datetime(2021, 1, 7, 15, 0, 3, 224676), null=True)),
                ('end', models.DateTimeField(blank=True, null=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('product', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='inventory.product', verbose_name='deal')),
            ],
        ),
    ]