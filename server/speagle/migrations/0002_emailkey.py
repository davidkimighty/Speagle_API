# Generated by Django 2.2.7 on 2019-11-11 18:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('speagle', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='EmailKey',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=254, unique=True, verbose_name='email')),
                ('key', models.CharField(blank=True, max_length=9, null=True, verbose_name='key')),
                ('count', models.IntegerField(default=0, verbose_name='count')),
            ],
        ),
    ]
