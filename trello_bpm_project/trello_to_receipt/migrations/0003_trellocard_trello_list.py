# Generated by Django 3.1.3 on 2020-11-27 03:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('trello_to_receipt', '0002_trellolist_board'),
    ]

    operations = [
        migrations.AddField(
            model_name='trellocard',
            name='trello_list',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='trello_to_receipt.trellolist'),
        ),
    ]
