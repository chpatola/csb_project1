# Generated by Django 3.1.2 on 2020-12-16 08:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0007_auditentry'),
    ]

    operations = [
        migrations.DeleteModel(
            name='AuditEntry',
        ),
        migrations.RemoveField(
            model_name='cities',
            name='population',
        ),
    ]
