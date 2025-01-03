# Generated by Django 5.1.2 on 2024-12-10 16:17

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('homepage', '0006_artwork_user'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment_body', models.TextField(blank=True, null=True)),
                ('date_create', models.DateField(auto_now_add=True)),
                ('comment_image', models.ImageField(upload_to='commentmedia/')),
                ('artwork_ref', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='homepage.artwork')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
