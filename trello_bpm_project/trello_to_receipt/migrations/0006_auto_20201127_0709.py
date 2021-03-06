# Generated by Django 3.1.3 on 2020-11-27 07:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trello_to_receipt', '0005_auto_20201127_0647'),
    ]

    operations = [
        migrations.CreateModel(
            name='CreatioReceipt',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('creatio_id', models.CharField(max_length=36, null=True, verbose_name='Creatio Id')),
                ('number', models.CharField(max_length=20, null=True, verbose_name='Number')),
            ],
        ),
        migrations.AddField(
            model_name='trelloboard',
            name='creatio_id',
            field=models.CharField(max_length=36, null=True, verbose_name='Creatio Id'),
        ),
        migrations.AddField(
            model_name='trellocard',
            name='creatio_id',
            field=models.CharField(max_length=36, null=True, verbose_name='Creatio Id'),
        ),
        migrations.AlterField(
            model_name='trellocard',
            name='trello_id',
            field=models.CharField(max_length=24, null=True, unique=True, verbose_name='Trello Id'),
        ),
    ]
