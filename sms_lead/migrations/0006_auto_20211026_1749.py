# Generated by Django 3.0 on 2021-10-27 00:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sms_lead', '0005_auto_20211026_1726'),
    ]

    operations = [
        migrations.AlterField(
            model_name='campaign',
            name='end',
            field=models.CharField(blank=True, db_index=True, max_length=254, null=True),
        ),
        migrations.AlterField(
            model_name='campaign',
            name='start',
            field=models.CharField(blank=True, db_index=True, max_length=254, null=True),
        ),
    ]