# Generated by Django 3.0.5 on 2020-05-26 21:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('agenda', '0009_auto_20200526_2322'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='sponsor',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='agenda.Sponsor'),
        ),
    ]