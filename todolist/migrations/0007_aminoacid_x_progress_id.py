# Generated by Django 2.2.2 on 2019-10-18 02:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('todolist', '0006_auto_20191011_2030'),
    ]

    operations = [
        migrations.AddField(
            model_name='aminoacid',
            name='X_Progress_ID',
            field=models.CharField(blank=True, default='', max_length=33),
        ),
    ]
