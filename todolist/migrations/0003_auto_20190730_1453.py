# Generated by Django 2.2.2 on 2019-07-30 20:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('todolist', '0002_auto_20190730_1444'),
    ]

    operations = [
        migrations.AddField(
            model_name='aminoacid',
            name='result',
            field=models.FileField(blank=True, null=True, upload_to='AminoAcid/fasta/'),
        ),
        migrations.AlterField(
            model_name='aminoacid',
            name='gc_richness_chunk_size',
            field=models.CharField(blank=True, max_length=20),
        ),
        migrations.AlterField(
            model_name='aminoacid',
            name='gc_richness_threshold',
            field=models.CharField(blank=True, max_length=20),
        ),
        migrations.AlterField(
            model_name='aminoacid',
            name='one_line_fasta',
            field=models.BooleanField(blank=True, default=False),
        ),
        migrations.AlterField(
            model_name='aminoacid',
            name='output',
            field=models.CharField(blank=True, default='out.fasta', max_length=20),
        ),
        migrations.AlterField(
            model_name='aminoacid',
            name='splice_sites',
            field=models.BooleanField(blank=True, default=False),
        ),
        migrations.AlterField(
            model_name='aminoacid',
            name='start_sites',
            field=models.BooleanField(blank=True, default=False),
        ),
        migrations.AlterField(
            model_name='aminoacid',
            name='verbose',
            field=models.IntegerField(blank=True),
        ),
    ]
