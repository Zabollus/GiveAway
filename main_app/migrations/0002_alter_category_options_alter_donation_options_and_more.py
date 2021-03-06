# Generated by Django 4.0.3 on 2022-04-06 23:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='category',
            options={'verbose_name': 'Kategoria', 'verbose_name_plural': 'Kategorie'},
        ),
        migrations.AlterModelOptions(
            name='donation',
            options={'verbose_name': 'Donacja', 'verbose_name_plural': 'Donacje'},
        ),
        migrations.AlterModelOptions(
            name='institution',
            options={'verbose_name': 'Instytucja', 'verbose_name_plural': 'Instytucje'},
        ),
        migrations.AddField(
            model_name='donation',
            name='is_taken',
            field=models.BooleanField(default=False, verbose_name='Odebrany'),
        ),
    ]
