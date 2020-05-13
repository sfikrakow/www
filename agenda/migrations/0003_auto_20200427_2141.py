# Generated by Django 3.0.5 on 2020-04-27 19:41

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailimages', '0001_squashed_0021'),
        ('wagtailcore', '0045_assign_unlock_grouppagepermission'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('contenttypes', '0002_remove_content_type_name'),
        ('agenda', '0002_auto_20200427_2117'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Categories',
            new_name='CategoryIndex',
        ),
        migrations.RenameModel(
            old_name='Events',
            new_name='EventIndex',
        ),
    ]