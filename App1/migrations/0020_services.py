# Generated by Django 5.1.1 on 2024-12-11 13:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('App1', '0019_vendor_location_vendor_updated_at_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Services',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Service_name', models.CharField(max_length=2000)),
                ('Service_category', models.CharField(max_length=2000)),
                ('Service_details', models.TextField()),
                ('Rate', models.IntegerField()),
                ('Image', models.URLField(blank=True, max_length=2000, null=True)),
            ],
        ),
    ]
