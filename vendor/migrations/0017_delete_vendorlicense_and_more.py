# Generated by Django 4.1 on 2023-12-13 03:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vendor', '0016_alter_vendorlicense_expiration_date_and_more'),
    ]

    operations = [
        migrations.DeleteModel(
            name='vendorLicense',
        ),
        migrations.AlterField(
            model_name='vendorrequest',
            name='expiration_date',
            field=models.DateField(blank=True, default='1990-01-01', null=True),
        ),
    ]
