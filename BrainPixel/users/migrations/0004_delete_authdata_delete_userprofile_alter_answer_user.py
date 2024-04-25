# Generated by Django 5.0.3 on 2024-04-25 21:04

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_alter_answer_user'),
    ]

    operations = [
        migrations.DeleteModel(
            name='AuthData',
        ),
        migrations.DeleteModel(
            name='UserProfile',
        ),
        migrations.AlterField(
            model_name='answer',
            name='user',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='users.user'),
        ),
    ]
