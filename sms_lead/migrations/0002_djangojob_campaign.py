# Generated by Django 3.0 on 2021-09-13 19:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('sms_lead', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='djangojob',
            name='campaign',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='sms_lead.Campaign'),
        ),
    ]
