# Generated by Django 5.2 on 2025-04-13 12:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('risks', '0008_riskhistory_riskresponse_userprofile'),
    ]

    operations = [
        migrations.AddField(
            model_name='riskresponse',
            name='currency',
            field=models.CharField(choices=[('USD', 'US Dollar ($)'), ('GBP', 'British Pound (£)'), ('EUR', 'Euro (€)'), ('INR', 'Indian Rupee (₹)')], default='USD', max_length=3),
        ),
    ]
