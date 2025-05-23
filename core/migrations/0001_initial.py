# Generated by Django 5.2 on 2025-05-16 03:22

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Team',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('team_name', models.CharField(max_length=255)),
                ('team_description', models.TextField(blank=True, null=True)),
                ('on_call', models.BooleanField(default=False)),
                ('shift_date', models.DateTimeField(blank=True, null=True)),
                ('shift_end_date', models.DateTimeField(blank=True, null=True)),
                ('leader', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='team_leader', to='accounts.profile')),
            ],
        ),
        migrations.CreateModel(
            name='Incident',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('urgency', models.IntegerField(choices=[(0, 'Low'), (1, 'Medium'), (2, 'High')], default=0)),
                ('status', models.CharField(choices=[('SUBMITTED', 'Submitted by Victim/Other'), ('PENDING_DOCTOR', 'Pending Doctor Approval'), ('PENDING_POLICE', 'Pending Police Acknowledgement'), ('ACKNOWLEDGED_POLICE', 'Acknowledged by Police'), ('REJECTED_DOCTOR', 'Rejected by Doctor'), ('REJECTED_POLICE', 'Rejected by Police'), ('RESOLVED', 'Resolved')], default='SUBMITTED', max_length=20)),
                ('triggered', models.BooleanField(default=False)),
                ('resolved', models.BooleanField(default=False)),
                ('title', models.CharField(max_length=255)),
                ('description', models.TextField(max_length=500)),
                ('Name_of_Patient', models.CharField(max_length=255)),
                ('Date_of_Accident', models.DateTimeField()),
                ('Date_of_Admission', models.DateTimeField()),
                ('doctor_approval_date', models.DateTimeField(blank=True, null=True)),
                ('doctor_comments', models.TextField(blank=True, null=True)),
                ('police_acknowledgement_date', models.DateTimeField(blank=True, null=True)),
                ('police_comments', models.TextField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('doctor_approved_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='doctor_approved_incidents', to='accounts.profile')),
                ('police_acknowledged_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='police_acknowledged_incidents', to='accounts.profile')),
                ('reported_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='reported_incidents', to='accounts.profile')),
                ('assigned_to', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='assigned_incidents', to='core.team')),
            ],
        ),
        migrations.CreateModel(
            name='TeamMember',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='member_of', to='accounts.profile')),
                ('team', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='members', to='core.team')),
            ],
        ),
    ]
