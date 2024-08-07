from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Wardrobe', '0002_alter_clothes_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='clothes',
            options={'verbose_name': 'Prenda', 'verbose_name_plural': 'Prendas'},
        ),
        migrations.AlterField(
            model_name='clothes',
            name='garment',
            field=models.ImageField(upload_to='Clothes/'),
        ),
        migrations.AlterField(
            model_name='clothes',
            name='type',
            field=models.CharField(choices=[('casual', 'Casual'), ('formal', 'Formal'), ('deportivo', 'Deportivo')], max_length=10),
        ),
    ]
