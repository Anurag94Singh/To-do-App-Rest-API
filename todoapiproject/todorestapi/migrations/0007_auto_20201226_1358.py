# Generated by Django 3.0 on 2020-12-26 08:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('todorestapi', '0006_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='taskmapping',
            name='student',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='student', to='todorestapi.Users'),
        ),
        migrations.AlterField(
            model_name='taskmapping',
            name='task',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='task', to='todorestapi.Tasks'),
        ),
        migrations.AlterField(
            model_name='tasks',
            name='createdby',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='createdby', to='todorestapi.Users'),
        ),
    ]
