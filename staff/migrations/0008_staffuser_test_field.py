# Generated by Django 4.2.11 on 2024-04-23 06:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('staff', '0007_rename_contrct_id_hireinfo_contract_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='staffuser',
            name='test_field',
            field=models.CharField(blank=True, default='', max_length=5, null=True),
        ),
    ]