# Generated by Django 5.1.3 on 2025-07-06 19:31

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('smart_todo', '0004_remove_todo_created_at_remove_todo_priority_score_and_more'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Todo',
        ),
        migrations.AddField(
            model_name='task',
            name='is_completed',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='category',
            name='tags',
            field=models.TextField(blank=True, help_text='Comma-separated tags'),
        ),
        migrations.AlterField(
            model_name='contextentry',
            name='source_type',
            field=models.CharField(choices=[('whatsapp', 'WhatsApp'), ('email', 'Email'), ('notes', 'Notes'), ('other', 'Other')], default='other', max_length=20),
        ),
        migrations.AlterField(
            model_name='task',
            name='category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='tasks', to='smart_todo.category'),
        ),
    ]
