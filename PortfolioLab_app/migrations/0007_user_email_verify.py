# Generated by Django 4.2.4 on 2023-09-19 09:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('PortfolioLab_app', '0006_user_alter_donation_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='email_verify',
            field=models.BooleanField(default=False),
        ),
    ]
