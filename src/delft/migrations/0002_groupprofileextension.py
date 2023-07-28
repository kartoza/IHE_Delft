# Generated by Django 3.2.18 on 2023-07-28 06:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('groups', '0034_auto_20200512_1431'),
        ('delft', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='GroupProfileExtension',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('featured', models.BooleanField(default=False, help_text='Show it to homepage.')),
                ('group_profile', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='groups.groupprofile')),
            ],
        ),
    ]