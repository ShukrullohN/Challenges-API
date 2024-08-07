# Generated by Django 5.0.7 on 2024-08-07 08:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('challenges', '0005_alter_tasksmodel_challenge_alter_membermodel_table_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='challengemodel',
            name='secret_password',
            field=models.CharField(blank=True, max_length=128, null=True),
        ),
        migrations.AlterField(
            model_name='challengemodel',
            name='status',
            field=models.BooleanField(default=True),
        ),
    ]
