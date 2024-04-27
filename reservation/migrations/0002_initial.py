# Generated by Django 4.2.11 on 2024-04-26 07:27

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('reservation', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='reservation',
            name='candidate',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reserved_by', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='reservation',
            name='company',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reservations', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='blockedcandidate',
            name='blocked_by',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='blocked_candidates_by', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='blockedcandidate',
            name='candidate',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='blocked_candidates', to=settings.AUTH_USER_MODEL),
        ),
    ]
