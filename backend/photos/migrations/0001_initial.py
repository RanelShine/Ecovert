# Generated by Django 5.2 on 2025-05-12 09:23

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Photo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='photos/')),
                ('latitude', models.FloatField()),
                ('longitude', models.FloatField()),
                ('date_uploaded', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
