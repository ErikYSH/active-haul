# Generated by Django 4.0.4 on 2022-04-29 01:17

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0010_alter_product_category_alter_product_conditions_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderitem',
            name='ordered',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='orderitem',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='product',
            name='category',
            field=models.CharField(choices=[('Headwears', 'Headwears'), ('T-shirts & Tops', 'T-shirt & Tops'), ('Shorts', 'Shorts'), ('Hoddies & Jackets', 'Hoddies & Jackets'), ('Leggings', 'Leggings'), ('Tank Tops', 'Tank Tops'), ('Gym Bags', 'Gym Bags'), ('Sports Bras', 'Sports Bras'), ('Crop Tops', 'Crop Tops'), ('Joggers', 'Joggers'), ('Bottoms', 'Bottoms'), ('Equipments', 'Equipments')], max_length=50),
        ),
        migrations.AlterField(
            model_name='product',
            name='conditions',
            field=models.CharField(choices=[('Used - Good', 'Used - Good'), ('Used - Fair', 'Used - Fair'), ('Used - Like New', 'Used - Like New'), ('New', 'New')], max_length=20),
        ),
        migrations.AlterField(
            model_name='product',
            name='main_category',
            field=models.CharField(choices=[('Womens', 'Womens'), ('Mens', 'Mens'), ('Accessories', 'Accessories')], max_length=30),
        ),
    ]
