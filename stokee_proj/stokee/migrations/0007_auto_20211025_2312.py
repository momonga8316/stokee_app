# Generated by Django 2.2.1 on 2021-10-25 14:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('stokee', '0006_tag_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='relationship',
            name='follower',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='follower', to='stokee.Profile'),
        ),
        migrations.AlterField(
            model_name='relationship',
            name='following',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='following', to='stokee.Profile'),
        ),
    ]
