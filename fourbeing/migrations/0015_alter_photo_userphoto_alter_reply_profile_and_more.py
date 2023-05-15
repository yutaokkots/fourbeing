# Generated by Django 4.2 on 2023-05-12 00:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('fourbeing', '0014_remove_profile_user'),
        ('useraccounts', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='photo',
            name='userPhoto',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='useraccounts.profile'),
        ),
        migrations.AlterField(
            model_name='reply',
            name='profile',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='useraccounts.profile'),
        ),
        migrations.DeleteModel(
            name='Profile',
        ),
    ]