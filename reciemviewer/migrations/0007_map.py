# Generated by Django 2.1.3 on 2018-11-29 00:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reciemviewer', '0006_auto_20181128_1745'),
    ]

    operations = [
        migrations.CreateModel(
            name='Map',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('layer', models.CharField(help_text='Capa', max_length=10)),
            ],
        ),
    ]
