# Generated by Django 2.1.3 on 2019-01-24 16:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0003_auto_20190124_1644'),
    ]

    operations = [
        migrations.RenameField(
            model_name='email',
            old_name='email',
            new_name='email_comma_separated',
        ),
    ]