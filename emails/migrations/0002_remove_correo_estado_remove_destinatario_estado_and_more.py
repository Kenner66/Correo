# Generated by Django 5.1.3 on 2024-11-06 23:34

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('emails', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RemoveField(
            model_name='correo',
            name='estado',
        ),
        migrations.RemoveField(
            model_name='destinatario',
            name='estado',
        ),
        migrations.RemoveField(
            model_name='destinatario',
            name='estado_lectura',
        ),
        migrations.AddField(
            model_name='correo',
            name='destinatarios',
            field=models.ManyToManyField(related_name='correos_recibidos', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='correo',
            name='asunto',
            field=models.CharField(max_length=200),
        ),
        migrations.AlterField(
            model_name='correo',
            name='remitente',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='enviados', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='destinatario',
            name='correo',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='destinatarios_emails', to='emails.correo'),
        ),
        migrations.AlterField(
            model_name='destinatario',
            name='usuario',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='destinatarios', to=settings.AUTH_USER_MODEL),
        ),
    ]
