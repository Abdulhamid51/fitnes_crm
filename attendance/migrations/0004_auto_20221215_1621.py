# Generated by Django 3.2.9 on 2022-12-15 16:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('attendance', '0003_monthname_number'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='month',
            name='month_name',
        ),
        migrations.DeleteModel(
            name='MonthName',
        ),
    ]