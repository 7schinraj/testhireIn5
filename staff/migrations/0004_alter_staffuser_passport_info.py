# Generated by Django 4.2.11 on 2024-04-19 05:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('staff', '0003_alter_passportinfo_passport_validity_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='staffuser',
            name='passport_info',
            field=models.ForeignKey(default='', null=True, on_delete=django.db.models.deletion.CASCADE, to='staff.passportinfo'),
        ),
    ]
