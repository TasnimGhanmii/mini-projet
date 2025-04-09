# Generated by Django 4.2 on 2025-04-09 11:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Formula',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('formula', models.CharField(default='courses + td + tp', max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Professor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('department', models.CharField(max_length=255)),
                ('grade', models.CharField(max_length=255)),
                ('courses', models.FloatField(default=0)),
                ('td', models.FloatField(default=0)),
                ('tp', models.FloatField(default=0)),
                ('coef', models.FloatField(default=0)),
                ('max_surveillance_hours', models.FloatField(default=0)),
                ('available', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='Session',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('session_id', models.CharField(max_length=10)),
                ('date', models.DateField()),
                ('time', models.TimeField()),
                ('professor_1', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='sessions_as_prof_1', to='surveillance_api.professor')),
                ('professor_2', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='sessions_as_prof_2', to='surveillance_api.professor')),
            ],
        ),
    ]
