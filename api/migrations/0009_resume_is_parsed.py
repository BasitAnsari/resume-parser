# Generated by Django 3.2.5 on 2021-07-25 19:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0008_resume_text'),
    ]

    operations = [
        migrations.AddField(
            model_name='resume',
            name='is_parsed',
            field=models.BooleanField(default=False),
        ),
    ]
