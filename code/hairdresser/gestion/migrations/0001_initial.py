# Generated by Django 4.2 on 2023-05-20 00:51

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Oferta',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=60)),
                ('fecha_fin', models.DateField(null=True)),
                ('descuento', models.FloatField()),
                ('activo', models.BooleanField(default=True)),
                ('updated', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'oferta',
                'verbose_name_plural': 'ofertas',
                'db_table': 'oferta',
            },
        ),
        migrations.CreateModel(
            name='Roles',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=255)),
                ('activo', models.BooleanField(default=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'roles',
                'verbose_name_plural': 'roles',
                'db_table': 'rol',
            },
        ),
        migrations.CreateModel(
            name='Ubicacion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=255)),
                ('updated', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'ubicacion',
                'verbose_name_plural': 'ubicaciones',
                'db_table': 'ubicacion',
            },
        ),
        migrations.CreateModel(
            name='Usuario',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('nombre', models.CharField(max_length=100)),
                ('apellidos', models.CharField(max_length=255)),
                ('password', models.CharField(max_length=500)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('movil', models.CharField(blank=True, max_length=9, null=True, validators=[django.core.validators.RegexValidator(message='El número de teléfono móvil debe longitud de 9.', regex='^\\d{9}$')])),
                ('fecha_nacimiento', models.DateField(null=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('activo', models.BooleanField(default=True)),
                ('role', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='gestion.roles')),
            ],
            options={
                'verbose_name': 'usuario',
                'verbose_name_plural': 'usuarios',
                'db_table': 'usuario',
            },
        ),
        migrations.CreateModel(
            name='Servicio',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=255)),
                ('descripcion', models.CharField(max_length=1000, null=True)),
                ('duracion', models.SmallIntegerField()),
                ('precio', models.FloatField()),
                ('activo', models.BooleanField(default=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('oferta', models.ManyToManyField(to='gestion.oferta')),
                ('ubicacion', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='gestion.ubicacion')),
            ],
            options={
                'verbose_name': 'servicio',
                'verbose_name_plural': 'servicios',
                'db_table': 'servicio',
            },
        ),
        migrations.CreateModel(
            name='Cita',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha_cita', models.DateField()),
                ('estado', models.CharField(choices=[('Programada', 'Programada'), ('Cancelada', 'Cancelada'), ('Realizada', 'Realizada')], default='Programada', max_length=12)),
                ('cliente', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='gestion.usuario')),
                ('servicio', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='gestion.servicio')),
            ],
            options={
                'verbose_name': 'cita',
                'verbose_name_plural': 'citas',
                'db_table': 'cita',
            },
        ),
        migrations.CreateModel(
            name='asigna_citas_empleado',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cita', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='gestion.cita')),
                ('empleado', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='gestion.usuario')),
            ],
            options={
                'verbose_name': 'asigna_citas_empleado',
                'db_table': 'asigna_citas_empleado',
            },
        ),
    ]
