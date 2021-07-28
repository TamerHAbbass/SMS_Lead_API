# Generated by Django 3.2.5 on 2021-07-28 01:49

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='SMS_Lead_Data',
            fields=[
                ('uuid', models.UUIDField(db_index=True, default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('Number', models.CharField(db_index=True, max_length=12)),
                ('Type', models.CharField(db_index=True, max_length=20)),
                ('Timezone', models.CharField(db_index=True, max_length=80)),
                ('First', models.CharField(db_index=True, max_length=100)),
                ('Last', models.CharField(db_index=True, max_length=100)),
                ('Address', models.CharField(db_index=True, max_length=254)),
                ('City', models.CharField(db_index=True, max_length=254)),
                ('State', models.CharField(db_index=True, max_length=254)),
                ('Zip', models.CharField(db_index=True, max_length=254)),
            ],
        ),
    ]
