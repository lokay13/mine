# Generated by Django 4.2.2 on 2023-06-25 13:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('miner', '0003_rename_efficiency_modifier_pickaxe_efficiency_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='pickaxe',
            field=models.ForeignKey(default=1, null=True, on_delete=django.db.models.deletion.SET_NULL, to='miner.pickaxe'),
        ),
    ]