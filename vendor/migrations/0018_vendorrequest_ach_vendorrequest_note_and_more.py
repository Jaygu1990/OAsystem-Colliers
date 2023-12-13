# Generated by Django 4.1 on 2023-12-13 03:10

from django.db import migrations, models
import vendor.models


class Migration(migrations.Migration):

    dependencies = [
        ('vendor', '0017_delete_vendorlicense_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='vendorrequest',
            name='ACH',
            field=models.FileField(blank=True, upload_to=vendor.models.upload_to_ACH),
        ),
        migrations.AddField(
            model_name='vendorrequest',
            name='Note',
            field=models.CharField(blank=True, max_length=256),
        ),
        migrations.AddField(
            model_name='vendorrequest',
            name='others',
            field=models.FileField(blank=True, upload_to=vendor.models.upload_to_others),
        ),
    ]
