# Generated by Django 3.1.3 on 2020-11-27 07:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trello_to_receipt', '0006_auto_20201127_0709'),
    ]

    operations = [
        migrations.AlterField(
            model_name='trellocard',
            name='trello_id',
            field=models.CharField(max_length=24, unique=True, verbose_name='Trello Id'),
        ),
    ]
