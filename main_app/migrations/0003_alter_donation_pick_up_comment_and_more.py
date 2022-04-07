# Generated by Django 4.0.3 on 2022-04-07 20:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0002_alter_category_options_alter_donation_options_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='donation',
            name='pick_up_comment',
            field=models.TextField(null=True, verbose_name='Komentarz do przesyłki'),
        ),
        migrations.AlterField(
            model_name='institution',
            name='type',
            field=models.CharField(choices=[('local collection', 'zbiórka lokalna'), ('non-governmental organization', ' organizacja pozarządowa'), ('foundation', 'fundacja')], default='foundation', max_length=32),
        ),
    ]
