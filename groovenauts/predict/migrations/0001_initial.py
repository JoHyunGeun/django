# Generated by Django 2.1.5 on 2019-01-24 12:21

from django.db import migrations, models
import predict.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Information',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='', max_length=10)),
                ('picture', models.ImageField(blank=True, default='default.jpeg', null=True, upload_to=predict.models.upload_location)),
            ],
        ),
    ]
