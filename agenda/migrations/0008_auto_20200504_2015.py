# Generated by Django 3.0.5 on 2020-05-04 18:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('agenda', '0007_auto_20200504_2011'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='date',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
