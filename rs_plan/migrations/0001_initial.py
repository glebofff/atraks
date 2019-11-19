# Generated by Django 2.2.7 on 2019-11-19 09:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Operator',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField(db_index=True)),
            ],
        ),
        migrations.CreateModel(
            name='Region',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField(db_index=True)),
            ],
        ),
        migrations.CreateModel(
            name='Plan',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pfx', models.CharField(db_index=True, max_length=3)),
                ('beg', models.CharField(db_index=True, max_length=7)),
                ('end', models.CharField(db_index=True, max_length=7)),
                ('capacity', models.SmallIntegerField(db_index=True)),
                ('operator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='rs_plan.Operator')),
                ('region', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='rs_plan.Region')),
            ],
        ),
    ]