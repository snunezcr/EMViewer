# Generated by Django 2.1.3 on 2018-11-28 22:06

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('reciemviewer', '0003_auto_20181110_1746'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contact',
            name='id',
            field=models.UUIDField(default=uuid.uuid4, help_text='Identificador único', primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='organization',
            name='id',
            field=models.UUIDField(default=uuid.uuid4, help_text='Identificador único', primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='service',
            name='id',
            field=models.UUIDField(default=uuid.uuid4, help_text='Identificador único', primary_key=True, serialize=False),
        ),
    ]
