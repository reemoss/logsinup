# Generated by Django 5.1.6 on 2025-02-15 04:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='droneuser',
            name='citizenship_upload',
            field=models.FileField(blank=True, null=True, upload_to='citizenship/', verbose_name='Upload Citizenship'),
        ),
        migrations.AlterField(
            model_name='droneuser',
            name='involvement_type',
            field=models.CharField(blank=True, choices=[('individual', 'Individual / Freelancer'), ('organizational', 'Organizational')], max_length=20, null=True, verbose_name='Involved as Organizational or Individual'),
        ),
    ]
