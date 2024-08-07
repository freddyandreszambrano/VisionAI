# Generated by Django 5.0.4 on 2024-06-13 04:29

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Clothes',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('garment', models.ImageField(upload_to='clothes/')),
                ('category', models.CharField(max_length=50)),
                ('dominant_color', models.TextField()),
                ('type', models.CharField(choices=[('casual', 'Casual'), ('formal', 'Formal'), ('Deportivo', 'Deportivo')], max_length=10)),
            ],
            options={
                'verbose_name': 'Prenda',
                'verbose_name_plural': 'Prendas',
            },
        ),
    ]
