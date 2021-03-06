# Generated by Django 3.1.2 on 2020-12-16 05:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0006_auto_20201215_1949'),
    ]

    operations = [
        migrations.CreateModel(
            name='AuditEntry',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('action', models.CharField(max_length=64)),
                ('ip', models.GenericIPAddressField(null=True)),
                ('username', models.CharField(max_length=256, null=True)),
            ],
        ),
    ]
