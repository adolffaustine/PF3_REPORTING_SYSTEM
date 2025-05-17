"""
    Creating Models for Incident Management System
"""
from django.db import models

from django.urls import reverse


from accounts.models import Profile

# Create your models here.

class Team(models.Model):
    """Model for team """
    team_name = models.CharField(max_length=255)
    team_description = models.TextField(blank=True, null=True)
    on_call = models.BooleanField(default=False)
    shift_date = models.DateTimeField(null=True, blank=True)
    shift_end_date = models.DateTimeField(null=True, blank=True)
    leader = models.ForeignKey(Profile, on_delete=models.SET_NULL, related_name="team_leader", null=True)
    def __str__(self):
        return f"{self.team_name} lead by {self.leader.user.username.title()}"
    
    def get_absolute_url(self):
        return reverse("core:teamDetail", args=[self.id])

class TeamMember(models.Model):
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name="members")
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="member_of")

    def __str__(self):
        return f"Member of team : {self.team.team_name}"

class Incident(models.Model):
    """Model for incidents happed"""
    class URGENCY_LEVEL(models.IntegerChoices):
        LOW = 0, 'Low'
        MEDIUM = 1, 'Medium'
        HIGH = 2, 'High'
        
    class INCIDENT_STATUS(models.TextChoices):
        SUBMITTED = 'SUBMITTED', 'Submitted by Victim/Other'
        PENDING_DOCTOR_APPROVAL = 'PENDING_DOCTOR', 'Pending Doctor Approval'
        PENDING_POLICE_ACKNOWLEDGEMENT = 'PENDING_POLICE', 'Pending Police Acknowledgement'
        ACKNOWLEDGED_BY_POLICE = 'ACKNOWLEDGED_POLICE', 'Acknowledged by Police'
        REJECTED_BY_DOCTOR = 'REJECTED_DOCTOR', 'Rejected by Doctor'
        REJECTED_BY_POLICE = 'REJECTED_POLICE', 'Rejected by Police'
        RESOLVED = 'RESOLVED', 'Resolved'


    
    urgency  = models.IntegerField(choices=URGENCY_LEVEL.choices, default=URGENCY_LEVEL.LOW)
    status = models.CharField(max_length=20, choices=INCIDENT_STATUS.choices, default=INCIDENT_STATUS.SUBMITTED)
    triggered = models.BooleanField(default=False)
    # acknowledged = models.BooleanField(default=False)
    resolved = models.BooleanField(default=False)
    title = models.CharField(max_length=255)
    description = models.TextField(max_length=500)
    Name_of_Patient = models.CharField(max_length=255)
    Date_of_Accident = models.DateTimeField(null=True, blank=True)
    Date_of_Admission = models.DateTimeField(null=True, blank=True)
    reported_by = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="reported_incidents", null=True, blank=True)
    assigned_to = models.ForeignKey(Team, on_delete=models.SET_NULL, related_name="assigned_incidents", null=True, blank=True)
    # Workflow fields
    doctor_approved_by = models.ForeignKey(Profile, on_delete=models.SET_NULL, related_name="doctor_approved_incidents", null=True, blank=True)
    doctor_approval_date = models.DateTimeField(null=True, blank=True)
    doctor_comments = models.TextField(blank=True, null=True)

    police_acknowledged_by = models.ForeignKey(Profile, on_delete=models.SET_NULL, related_name="police_acknowledged_incidents", null=True, blank=True)
    police_acknowledgement_date = models.DateTimeField(null=True, blank=True)
    police_comments = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title}"
    
    def get_absolute_url(self):
        return reverse("core:detailIncident", args=[self.id])
    
    @property
    def is_acknowledged_by_police(self):
        return self.police_acknowledged_by is not None and self.status == self.INCIDENT_STATUS.ACKNOWLEDGED_BY_POLICE

    @property
    def is_approved_by_doctor(self):
        return self.doctor_approved_by is not None and self.status not in [self.INCIDENT_STATUS.SUBMITTED, self.INCIDENT_STATUS.PENDING_DOCTOR_APPROVAL, self.INCIDENT_STATUS.REJECTED_BY_DOCTOR]