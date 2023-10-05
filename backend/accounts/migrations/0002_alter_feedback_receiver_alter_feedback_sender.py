# Generated by Django 4.2.5 on 2023-10-05 01:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='feedback',
            name='receiver',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='feedbacks_receiver', to='accounts.accountsuser'),
        ),
        migrations.AlterField(
            model_name='feedback',
            name='sender',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='feedbacks_sender', to='accounts.accountsuser'),
        ),
    ]