# Generated by Django 4.2.5 on 2023-10-04 06:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='accountsuser',
            name='reward_points',
            field=models.IntegerField(default=0),
        ),
    ]