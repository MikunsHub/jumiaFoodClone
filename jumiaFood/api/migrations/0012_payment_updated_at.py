# Generated by Django 4.0.6 on 2022-08-02 10:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0011_payment'),
    ]

    operations = [
        migrations.AddField(
            model_name='payment',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
    ]