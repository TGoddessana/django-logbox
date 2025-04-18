# Generated by Django 4.2.19 on 2025-03-31 12:17

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("auth", "__first__"),
        ("django_logbox", "0006_backfill_device_os_browser_fields"),
    ]

    operations = [
        migrations.AddField(
            model_name="serverlog",
            name="user",
            field=models.ForeignKey(
                blank=True,
                help_text="User associated with the request, if authenticated.",
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="server_logs",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AlterField(
            model_name="serverlog",
            name="querystring",
            field=models.TextField(
                help_text="Query parameters of the request as a URL-encoded string, e.g., 'param1=value1&ampparam2=value2'.",
                null=True,
                verbose_name="querystring",
            ),
        ),
    ]
