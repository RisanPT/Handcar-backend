# Generated by Django 5.1.1 on 2024-10-22 06:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('App1', '0004_subscription'),
    ]

    operations = [
        migrations.AddField(
            model_name='subscription',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
    ]
