# Generated by Django 3.2.5 on 2022-01-31 21:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bookclub', '0002_alter_user_location'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='age',
            field=models.IntegerField(blank=True),
        ),
    ]
