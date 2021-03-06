# Generated by Django 3.1.3 on 2020-11-27 06:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trello_to_receipt', '0004_trelloboard_url'),
    ]

    operations = [
        migrations.AlterField(
            model_name='trellocard',
            name='title',
            field=models.CharField(max_length=255, null=True, verbose_name='Card title'),
        ),
        migrations.AlterField(
            model_name='trellocard',
            name='trello_id',
            field=models.CharField(max_length=24, null=True, verbose_name='Trello Id'),
        ),
        migrations.AlterField(
            model_name='trellocard',
            name='url',
            field=models.CharField(max_length=500, null=True, verbose_name='Card link'),
        ),
    ]
