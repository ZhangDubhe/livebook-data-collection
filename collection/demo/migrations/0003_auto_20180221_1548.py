# Generated by Django 2.0.1 on 2018-02-21 22:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('demo', '0002_disease_concept_type'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='value',
            unique_together={('disease', 'symptom', 'property')},
        ),
    ]