# Generated by Django 3.2.5 on 2021-07-18 11:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_alter_resume_phone'),
    ]

    operations = [
        migrations.AlterField(
            model_name='resume',
            name='designation',
            field=models.CharField(max_length=1024, null=True),
        ),
        migrations.AlterField(
            model_name='resume',
            name='skills',
            field=models.CharField(max_length=1024, null=True),
        ),
    ]
