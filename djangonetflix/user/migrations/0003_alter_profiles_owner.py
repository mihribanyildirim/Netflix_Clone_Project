# Generated by Django 3.2.13 on 2022-09-21 12:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0002_profil'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profiles',
            name='owner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.profil'),
        ),
    ]
