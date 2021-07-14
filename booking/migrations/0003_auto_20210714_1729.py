# Generated by Django 3.2.5 on 2021-07-14 15:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('booking', '0002_coworker'),
    ]

    operations = [
        migrations.AlterField(
            model_name='coworker',
            name='current_projects',
            field=models.CharField(blank=True, max_length=1000),
        ),
        migrations.AlterField(
            model_name='coworker',
            name='description',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='coworker',
            name='profile_image',
            field=models.ImageField(blank=True, upload_to=''),
        ),
    ]
