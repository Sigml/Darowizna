# Generated by Django 4.2.4 on 2023-09-17 11:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('PortfolioLab_app', '0004_donation_is_taken'),
    ]

    operations = [
        migrations.AddField(
            model_name='donation',
            name='taken_timestamp',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
