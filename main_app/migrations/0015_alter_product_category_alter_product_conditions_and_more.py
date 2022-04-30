# Generated by Django 4.0.4 on 2022-04-30 19:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0014_alter_product_category_alter_product_conditions_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='category',
            field=models.CharField(choices=[('Sports Bras', 'Sports Bras'), ('Shorts', 'Shorts'), ('Joggers', 'Joggers'), ('T-shirts & Tops', 'T-shirt & Tops'), ('Tank Tops', 'Tank Tops'), ('Gym Bags', 'Gym Bags'), ('Equipments', 'Equipments'), ('Hoddies & Jackets', 'Hoddies & Jackets'), ('Crop Tops', 'Crop Tops'), ('Headwears', 'Headwears'), ('Leggings', 'Leggings'), ('Bottoms', 'Bottoms')], max_length=50),
        ),
        migrations.AlterField(
            model_name='product',
            name='conditions',
            field=models.CharField(choices=[('Used - Like New', 'Used - Like New'), ('New', 'New'), ('Used - Good', 'Used - Good'), ('Used - Fair', 'Used - Fair')], max_length=20),
        ),
        migrations.AlterField(
            model_name='product',
            name='main_category',
            field=models.CharField(choices=[('Mens', 'Mens'), ('Accessories', 'Accessories'), ('Womens', 'Womens')], max_length=30),
        ),
        migrations.AlterField(
            model_name='product',
            name='slug',
            field=models.SlugField(unique=True),
        ),
    ]
