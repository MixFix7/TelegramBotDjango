# Generated by Django 4.2.6 on 2023-10-10 16:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("chats", "0002_remove_chat_chat_id"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="chat",
            name="chat_username",
        ),
        migrations.AddField(
            model_name="chat",
            name="chat_user_id",
            field=models.CharField(default=None, max_length=100),
            preserve_default=False,
        ),
    ]
