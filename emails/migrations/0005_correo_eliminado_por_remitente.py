# Generated by Django 5.1.3 on 2024-11-14 20:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('emails', '0004_remove_correo_destinatarios_correo_destinatario'),
    ]

    operations = [
        migrations.AddField(
            model_name='correo',
            name='eliminado_por_remitente',
            field=models.BooleanField(default=False),
        ),
    ]
