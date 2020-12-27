# Generated by Django 3.0 on 2020-12-25 17:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='TaskStatus',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=60)),
            ],
        ),
        migrations.CreateModel(
            name='Users',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=60)),
                ('role', models.CharField(max_length=60)),
            ],
        ),
        migrations.CreateModel(
            name='Tasks',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=60)),
                ('description', models.CharField(max_length=200)),
                ('createdby', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='todorestapi.Users')),
                ('status', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='todorestapi.TaskStatus')),
            ],
        ),
        migrations.CreateModel(
            name='TaskMapping',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(max_length=60)),
                ('studentid', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='todorestapi.Users')),
                ('taskid', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='todorestapi.Tasks')),
            ],
        ),
    ]
