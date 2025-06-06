# Generated by Django 5.2 on 2025-04-19 21:15

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('playground', '0003_enseignant_total_enseignant_total_r_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='session',
            name='professor_1',
        ),
        migrations.RemoveField(
            model_name='session',
            name='professor_2',
        ),
        migrations.RemoveField(
            model_name='session',
            name='professor_3',
        ),
        migrations.AlterField(
            model_name='session',
            name='nb_salle',
            field=models.IntegerField(verbose_name=2),
        ),
        migrations.CreateModel(
            name='Affectation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('role', models.CharField(choices=[('S', 'Surveillant'), ('RS', 'Responsable + Surveillant'), ('R', 'Responsable Seulement')], max_length=2, verbose_name='Rôle')),
                ('enseignant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='affectations', to='playground.enseignant', verbose_name='Enseignant')),
                ('session', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='affectations', to='playground.session', verbose_name="Session d'Examen")),
            ],
            options={
                'verbose_name': 'Affectation',
                'verbose_name_plural': 'Affectations',
                'unique_together': {('session', 'enseignant')},
            },
        ),
    ]
