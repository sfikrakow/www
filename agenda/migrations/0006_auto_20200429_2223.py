# Generated by Django 3.0.5 on 2020-04-29 20:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('agenda', '0005_auto_20200429_2220'),
    ]

    operations = [
        migrations.AlterField(
            model_name='edition',
            name='end_date',
            field=models.DateTimeField(blank=True, null=True, verbose_name='Edition end date'),
        ),
        migrations.AlterField(
            model_name='edition',
            name='start_date',
            field=models.DateTimeField(blank=True, null=True, verbose_name='Edition start date'),
        ),
    ]