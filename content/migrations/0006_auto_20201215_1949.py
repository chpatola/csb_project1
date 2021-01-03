# Generated by Django 3.1.2 on 2020-12-15 16:49

from django.db import migrations, models
import fernet_fields.fields


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0005_auto_20201215_1902'),
    ]

    operations = [
        migrations.CreateModel(
            name='OurUsers',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('social_security', fernet_fields.fields.EncryptedTextField(max_length=11)),
                ('my_issue', models.TextField()),
            ],
            options={
                'db_table': 'OURUSERS',
            },
        ),
        migrations.DeleteModel(
            name='User',
        ),
        migrations.AlterField(
            model_name='userdata',
            name='social_security',
            field=models.CharField(max_length=11),
        ),
        migrations.AlterModelTable(
            name='userdata',
            table='USERDATA',
        ),
    ]
