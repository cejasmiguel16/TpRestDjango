# Generated by Django 4.2.1 on 2023-05-25 18:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('stock', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Orden',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha_hora', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='DetalleOrden',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cantidad', models.IntegerField()),
                ('orden', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='orden.orden')),
                ('productos', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='stock.producto')),
            ],
        ),
    ]
