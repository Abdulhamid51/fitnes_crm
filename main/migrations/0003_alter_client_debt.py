# Generated by Django 3.2.9 on 2022-12-15 16:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_client_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='client',
            name='debt',
            field=models.BooleanField(default=True, verbose_name='Qarzi bor'),
        ),
    ]
