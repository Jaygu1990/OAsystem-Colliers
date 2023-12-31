# Generated by Django 4.1 on 2023-12-11 07:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='vendorRequest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('deal_numer', models.PositiveIntegerField()),
                ('vendor_name', models.CharField(max_length=256)),
                ('vendor_address', models.CharField(max_length=256)),
                ('W9', models.FileField(upload_to='PDF/W9/')),
                ('request_person', models.CharField(max_length=256)),
                ('prepare_person', models.CharField(max_length=256)),
                ('approve_person', models.CharField(max_length=256)),
            ],
        ),
        migrations.CreateModel(
            name='eachVendor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('TIN_check', models.FileField(upload_to='PDF/TIN/')),
                ('license_check', models.FileField(upload_to='PDF/License/')),
                ('vendor_request', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='vendor.vendorrequest')),
            ],
        ),
    ]
