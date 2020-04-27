from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ('pages', '0003_auto_20200427_2015'),
    ]

    operations = [
        migrations.RunSQL('DROP TABLE IF EXISTS home_homepage')
    ]
