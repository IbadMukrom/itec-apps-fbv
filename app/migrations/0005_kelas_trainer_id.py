# Generated by Django 3.1 on 2020-09-04 12:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_auto_20200904_2013'),
    ]

    operations = [
        migrations.AddField(
            model_name='kelas',
            name='trainer_id',
            field=models.PositiveBigIntegerField(blank=True, null=True),
        ),
    ]