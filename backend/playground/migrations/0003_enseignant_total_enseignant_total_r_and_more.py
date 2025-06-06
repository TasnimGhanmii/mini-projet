# Generated by Django 5.2 on 2025-04-19 18:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('playground', '0002_session_professor_3'),
    ]

    operations = [
        migrations.AddField(
            model_name='enseignant',
            name='total',
            field=models.IntegerField(default=0, verbose_name='Total Général'),
        ),
        migrations.AddField(
            model_name='enseignant',
            name='total_R',
            field=models.IntegerField(default=0, verbose_name='Total Responsabilité'),
        ),
        migrations.AddField(
            model_name='enseignant',
            name='total_RS',
            field=models.IntegerField(default=0, verbose_name='Total Responsabilité de Surveillance'),
        ),
        migrations.AddField(
            model_name='enseignant',
            name='total_S',
            field=models.IntegerField(default=0, verbose_name='Total Surveillance'),
        ),
        migrations.AlterField(
            model_name='enseignant',
            name='grade',
            field=models.CharField(max_length=100, verbose_name='Grade'),
        ),
    ]
