# Generated by Django 3.1.3 on 2020-11-27 20:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trello_to_receipt', '0008_auto_20201127_1846'),
    ]

    operations = [
        migrations.AddField(
            model_name='executor',
            name='full_name',
            field=models.CharField(max_length=150, null=True, verbose_name='Name'),
        ),
    ]
