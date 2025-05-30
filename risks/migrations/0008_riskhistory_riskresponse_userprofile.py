# Generated by Django 5.2 on 2025-04-13 05:01

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('risks', '0007_remove_risk_created_by'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='RiskHistory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('description', models.TextField(blank=True)),
                ('category_name', models.CharField(max_length=100)),
                ('likelihood', models.IntegerField()),
                ('impact', models.IntegerField()),
                ('status', models.CharField(max_length=20)),
                ('owner', models.CharField(blank=True, max_length=100)),
                ('changed_at', models.DateTimeField(auto_now_add=True)),
                ('change_comment', models.TextField(blank=True)),
                ('changed_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
                ('risk', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='history', to='risks.risk')),
            ],
            options={
                'verbose_name_plural': 'Risk histories',
                'ordering': ['-changed_at'],
            },
        ),
        migrations.CreateModel(
            name='RiskResponse',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('response_type', models.CharField(choices=[('Avoid', 'Avoid'), ('Transfer', 'Transfer'), ('Mitigate', 'Mitigate'), ('Accept', 'Accept')], max_length=20)),
                ('description', models.TextField()),
                ('cost_estimate', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('responsible_person', models.CharField(max_length=100)),
                ('target_date', models.DateField(blank=True, null=True)),
                ('status', models.CharField(choices=[('Planned', 'Planned'), ('In Progress', 'In Progress'), ('Completed', 'Completed')], default='Planned', max_length=20)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('created_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='created_responses', to=settings.AUTH_USER_MODEL)),
                ('risk', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='responses', to='risks.risk')),
            ],
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('role', models.CharField(choices=[('viewer', 'Viewer'), ('contributor', 'Contributor'), ('manager', 'Manager'), ('admin', 'Administrator')], default='contributor', max_length=20)),
                ('projects', models.ManyToManyField(blank=True, related_name='team_members', to='risks.project')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='profile', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
