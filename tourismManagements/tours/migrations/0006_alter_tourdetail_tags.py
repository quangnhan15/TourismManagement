# Generated by Django 5.0.4 on 2024-05-23 07:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tours', '0005_alter_user_avatar'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tourdetail',
            name='tags',
            field=models.ManyToManyField(blank=True, related_name='tourdetails', to='tours.tag'),
        ),
    ]
