# Generated by Django 3.2 on 2021-05-10 02:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('imgdb', '0005_imagedata_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='imagedata',
            name='path',
            field=models.CharField(blank=True, max_length=512, null=True),
        ),
    ]
