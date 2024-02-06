# Generated by Django 5.0.1 on 2024-01-25 16:55

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0008_bankuser_pfp'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bankuser',
            name='pfp',
            field=models.ImageField(blank=True, null=True, upload_to='base/static/base/images'),
        ),
        migrations.CreateModel(
            name='Recipient',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=20)),
                ('last_name', models.CharField(max_length=20)),
                ('account_number', models.IntegerField()),
                ('no_of_transfers', models.IntegerField(default=0)),
                ('bankuser', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='base.bankuser')),
            ],
        ),
    ]