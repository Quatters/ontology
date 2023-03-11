# Generated by Django 4.1.7 on 2023-03-11 05:11

from django.db import migrations, models
import django.db.models.deletion
import vstutils.models.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('ontology', '0001_create_admin'),
    ]

    operations = [
        migrations.CreateModel(
            name='Area',
            fields=[
                ('id', models.AutoField(max_length=20, primary_key=True, serialize=False)),
                ('hidden', models.BooleanField(default=False)),
                ('name', models.CharField(db_index=True, max_length=64)),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Cargo',
            fields=[
                ('id', models.AutoField(max_length=20, primary_key=True, serialize=False)),
                ('hidden', models.BooleanField(default=False)),
                ('mass', models.FloatField()),
                ('type', models.CharField(db_index=True, max_length=24)),
            ],
        ),
        migrations.CreateModel(
            name='ComputedRoute',
            fields=[
                ('id', models.AutoField(max_length=20, primary_key=True, serialize=False)),
                ('hidden', models.BooleanField(default=False)),
                ('fuel', models.FloatField()),
                ('path', models.JSONField(default=list)),
            ],
            options={
                'default_related_name': 'computed_routes',
            },
        ),
        migrations.CreateModel(
            name='Route',
            fields=[
                ('id', models.AutoField(max_length=20, primary_key=True, serialize=False)),
                ('hidden', models.BooleanField(default=False)),
                ('distance', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='Truck',
            fields=[
                ('id', models.AutoField(max_length=20, primary_key=True, serialize=False)),
                ('hidden', models.BooleanField(default=False)),
                ('number', models.CharField(db_index=True, max_length=16, unique=True)),
                ('type', models.CharField(db_index=True, max_length=24)),
            ],
            options={
                'ordering': ['number'],
                'default_related_name': 'trucks',
            },
        ),
        migrations.CreateModel(
            name='TruckModel',
            fields=[
                ('id', models.AutoField(max_length=20, primary_key=True, serialize=False)),
                ('hidden', models.BooleanField(default=False)),
                ('name', models.CharField(db_index=True, max_length=64)),
                ('load_capacity', models.FloatField()),
                ('gas_tank_capacity', models.FloatField()),
                ('fuel_consumption', models.FloatField()),
            ],
            options={
                'ordering': (['name'],),
            },
        ),
        migrations.AddConstraint(
            model_name='truckmodel',
            constraint=models.CheckConstraint(check=models.Q(('load_capacity__gt', 0)), name='load_capacity_gt0'),
        ),
        migrations.AddConstraint(
            model_name='truckmodel',
            constraint=models.CheckConstraint(check=models.Q(('gas_tank_capacity__gt', 0)), name='gas_tank_capacity_gt0'),
        ),
        migrations.AddConstraint(
            model_name='truckmodel',
            constraint=models.CheckConstraint(check=models.Q(('fuel_consumption__gt', 0)), name='fuel_consumption_gt0'),
        ),
        migrations.AddConstraint(
            model_name='truckmodel',
            constraint=models.CheckConstraint(check=models.Q(('gas_tank_capacity__gt', models.F('fuel_consumption'))), name='gas_tank_capacity_gt_fuel_consumption'),
        ),
        migrations.AddField(
            model_name='truck',
            name='location',
            field=vstutils.models.fields.FkModelField(on_delete=django.db.models.deletion.CASCADE, to='ontology.area'),
        ),
        migrations.AddField(
            model_name='truck',
            name='model',
            field=vstutils.models.fields.FkModelField(on_delete=django.db.models.deletion.CASCADE, to='ontology.truckmodel'),
        ),
        migrations.AddField(
            model_name='route',
            name='wherefrom',
            field=vstutils.models.fields.FkModelField(on_delete=django.db.models.deletion.CASCADE, related_name='wherefrom_routes', to='ontology.area'),
        ),
        migrations.AddField(
            model_name='route',
            name='whereto',
            field=vstutils.models.fields.FkModelField(on_delete=django.db.models.deletion.CASCADE, related_name='whereto_routes', to='ontology.area'),
        ),
        migrations.AddField(
            model_name='computedroute',
            name='cargo',
            field=vstutils.models.fields.FkModelField(on_delete=django.db.models.deletion.CASCADE, to='ontology.cargo'),
        ),
        migrations.AddField(
            model_name='computedroute',
            name='truck',
            field=vstutils.models.fields.FkModelField(on_delete=django.db.models.deletion.CASCADE, to='ontology.truck'),
        ),
        migrations.AddField(
            model_name='cargo',
            name='destination',
            field=vstutils.models.fields.FkModelField(on_delete=django.db.models.deletion.CASCADE, related_name='cargos_destination', to='ontology.area'),
        ),
        migrations.AddField(
            model_name='cargo',
            name='location',
            field=vstutils.models.fields.FkModelField(on_delete=django.db.models.deletion.CASCADE, related_name='cargos_location', to='ontology.area'),
        ),
        migrations.AddConstraint(
            model_name='route',
            constraint=models.CheckConstraint(check=models.Q(('wherefrom', models.F('whereto')), _negated=True), name='different_wherefrom_whereto'),
        ),
        migrations.AddConstraint(
            model_name='route',
            constraint=models.CheckConstraint(check=models.Q(('distance__gt', 0)), name='distance_gt0'),
        ),
        migrations.AddConstraint(
            model_name='route',
            constraint=models.UniqueConstraint(fields=('wherefrom', 'whereto'), name='unique_wherefrom_whereto'),
        ),
        migrations.AddConstraint(
            model_name='cargo',
            constraint=models.CheckConstraint(check=models.Q(('location', models.F('destination')), _negated=True), name='different_location_destination'),
        ),
        migrations.AddConstraint(
            model_name='cargo',
            constraint=models.CheckConstraint(check=models.Q(('mass__gt', 0)), name='mass_gt0'),
        ),
    ]