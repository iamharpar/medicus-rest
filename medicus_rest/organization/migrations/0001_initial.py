# Generated by Django 3.0.2 on 2020-01-13 10:09

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Organization',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('name', models.CharField(max_length=30, unique=True, verbose_name='organization name')),
                ('description', models.TextField(verbose_name='proper description of organization')),
            ],
        ),
    ]
