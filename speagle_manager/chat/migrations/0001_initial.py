# Generated by Django 2.2.7 on 2019-12-03 07:09

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('hash_id', models.CharField(default='a71f059aabb2c07ae7adb6b66038509f', max_length=50, unique=True, verbose_name='hashed id')),
                ('text', models.TextField()),
                ('timestamp', models.DateTimeField(auto_now_add=True, verbose_name='sent datetime')),
                ('sender', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='sender')),
            ],
        ),
        migrations.CreateModel(
            name='MessageThread',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50, unique=True, verbose_name='title')),
                ('timestamp', models.DateTimeField(auto_now_add=True, verbose_name='created')),
                ('unread_messages', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='chat.Message', verbose_name='unread messages')),
                ('users', models.ManyToManyField(blank=True, to=settings.AUTH_USER_MODEL, verbose_name='users')),
            ],
        ),
        migrations.CreateModel(
            name='Unreads',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField(auto_now_add=True, verbose_name='sent datetime')),
                ('message', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='unread', to='chat.Message')),
                ('recipient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='unread', to=settings.AUTH_USER_MODEL)),
                ('thread', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='unread', to='chat.MessageThread')),
            ],
        ),
        migrations.AddField(
            model_name='message',
            name='thread',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='messages', to='chat.MessageThread', verbose_name='thread'),
        ),
    ]