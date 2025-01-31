# Generated by Django 5.1.5 on 2025-01-31 11:37

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("LittleLemonAPI", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="cart",
            name="price",
            field=models.DecimalField(decimal_places=2, editable=False, max_digits=6),
        ),
        migrations.AlterField(
            model_name="orderitem",
            name="order",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="LittleLemonAPI.order"
            ),
        ),
    ]
