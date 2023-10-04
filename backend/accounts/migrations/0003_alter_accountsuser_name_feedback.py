# Generated by Django 4.2.5 on 2023-10-04 07:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_alter_accountsuser_reward_points'),
    ]

    operations = [
        migrations.AlterField(
            model_name='accountsuser',
            name='name',
            field=models.CharField(blank=True, max_length=255, null=True, unique=True),
        ),
        migrations.CreateModel(
            name='Feedback',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('insight', models.CharField(blank=True, max_length=255, null=True)),
                ('recommendation', models.CharField(blank=True, max_length=255, null=True)),
                ('response', models.CharField(blank=True, max_length=255, null=True)),
                ('receiver', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='feedbacks', to='accounts.accountsuser')),
            ],
        ),
    ]