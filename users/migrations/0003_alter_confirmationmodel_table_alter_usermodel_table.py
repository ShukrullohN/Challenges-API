# Generated by Django 5.0.7 on 2024-08-07 07:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_alter_confirmationmodel_options_and_more'),
    ]

    operations = [
        migrations.AlterModelTable(
            name='confirmationmodel',
            table='confirmation',
        ),
        migrations.AlterModelTable(
            name='usermodel',
            table='users',
        ),
    ]