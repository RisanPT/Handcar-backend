# Generated by Django 5.1.1 on 2024-10-22 05:54

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('App1', '0003_product_created_at'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Subscription',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('plan', models.CharField(choices=[('basic', 'Basic'), ('premium', 'Premium'), ('luxury', 'Luxury')], max_length=10)),
                ('category', models.CharField(choices=[('car_wash', 'Car Wash'), ('maintenance', 'Maintenance')], max_length=15)),
                ('duration_months', models.IntegerField()),
                ('start_date', models.DateField(auto_now_add=True)),
                ('end_date', models.DateField()),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
