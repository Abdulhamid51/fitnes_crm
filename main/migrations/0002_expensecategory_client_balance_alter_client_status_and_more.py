# Generated by Django 4.0.5 on 2023-01-19 05:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ExpenseCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('created', models.DateField(auto_now_add=True, verbose_name="Qo'shilgan sana")),
            ],
        ),
        migrations.AddField(
            model_name='client',
            name='balance',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='client',
            name='status',
            field=models.CharField(blank=True, choices=[('ACTIVE', 'Faol'), ('INACTIVE', 'Faolmas'), ('PAUSED', 'Pauza')], max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='client',
            name='uid',
            field=models.SlugField(blank=True, unique=True),
        ),
        migrations.CreateModel(
            name='Expense',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('summa', models.IntegerField(default=0)),
                ('info', models.TextField(blank=True, null=True)),
                ('created', models.DateField(auto_now_add=True, verbose_name="Qo'shilgan sana")),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='expense_category', to='main.expensecategory')),
            ],
        ),
    ]
