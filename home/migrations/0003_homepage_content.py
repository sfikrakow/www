# Generated by Django 3.0.5 on 2020-04-19 11:30

from django.db import migrations
import wagtail.core.fields


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0002_create_homepage'),
    ]

    operations = [
        migrations.AddField(
            model_name='homepage',
            name='content',
            field=wagtail.core.fields.RichTextField(default=''),
            preserve_default=False,
        ),
    ]