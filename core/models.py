"""
    Creating Models for Incident Management System
"""
from django.db import models

from django.urls import reverse


from accounts.models import Profile,Hospital

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

class PoliceStation(models.Model):
    name = models.CharField(max_length=255, unique=True)
    location_details = models.TextField(blank=True, null=True, verbose_name="Location/Address Details")
    contact_phone = models.CharField(max_length=20, blank=True, null=True)
    contact_email = models.EmailField(blank=True, null=True)

    def __str__(self):
        return self.name

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
    case_file_no = models.CharField(max_length=100, blank=True, null=True, verbose_name="Case File No.")
    police_station = models.ForeignKey(PoliceStation, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Police Station")
    # acknowledged = models.BooleanField(default=False)
    resolved = models.BooleanField(default=False)
    Incident_Type = models.CharField(max_length=255)
    description = models.TextField(max_length=500)
    Name_of_Patient = models.CharField(max_length=255)
    Date_of_Accident = models.DateTimeField(null=True, blank=True)
    Date_of_Admission = models.DateTimeField(null=True, blank=True)
    reported_by = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="reported_incidents", null=True, blank=True)
    assigned_to = models.ForeignKey(Team, on_delete=models.SET_NULL, related_name="assigned_incidents", null=True, blank=True)
    hospital = models.ForeignKey(Hospital, on_delete=models.SET_NULL, null=True, blank=True, related_name="incidents_at_hospital")
    doctor_approved_by = models.ForeignKey(Profile, on_delete=models.SET_NULL, related_name="doctor_approved_incidents", null=True, blank=True)
    doctor_approval_date = models.DateTimeField(null=True, blank=True)
    doctor_comments = models.TextField(blank=True, null=True)

    police_acknowledged_by = models.ForeignKey(Profile, on_delete=models.SET_NULL, related_name="police_acknowledged_incidents", null=True, blank=True)
    police_acknowledgement_date = models.DateTimeField(null=True, blank=True)
    police_comments = models.TextField(blank=True, null=True)
    # New fields for police assignment and contact sharing
    assigned_police_officer = models.ForeignKey(Profile, on_delete=models.SET_NULL, related_name="assigned_cases", null=True, blank=True, verbose_name="Assigned Police Officer")
    contact_details_for_hospital = models.TextField(blank=True, null=True, verbose_name="Contact Details for Hospital (from Police)")
    contact_details_for_police = models.TextField(blank=True, null=True, verbose_name="Contact Details for Police (from Hospital/Doctor)")
      # Fields for PART II: Medical Details
    patient_file_no = models.CharField(max_length=100, blank=True, null=True, verbose_name="Patient File No.")
    nature_of_complaint = models.TextField(blank=True, null=True, verbose_name="Nature of Complaint")
    estimated_age = models.CharField(max_length=50, blank=True, null=True, verbose_name="Estimated Age")
    general_physical_mental_examination = models.TextField(blank=True, null=True, verbose_name="General Physical/Mental Examination")
    medical_history = models.TextField(blank=True, null=True, verbose_name="Medical History")
    condition_appearance_of_clothes = models.TextField(blank=True, null=True, verbose_name="Condition/Appearance of Clothes (blood, tears, fluids, etc.)")
    guardian_name = models.CharField(max_length=255, blank=True, null=True, verbose_name="Name of Guardian")
    guardian_relationship = models.CharField(max_length=100, blank=True, null=True, verbose_name="Relationship of Guardian")
    # Fields for PART III: Assault, Accident and Other Cases
    approx_age_of_injury = models.CharField(max_length=100, blank=True, null=True, verbose_name="Approximately Age of Injury")
    treatment_received = models.TextField(blank=True, null=True, verbose_name="Treatment if Received Any")
    description_of_site_situation_depth_of_injury = models.TextField(blank=True, null=True, verbose_name="Description of Site, Situation and Depth of Injury Sustained")
    type_of_weapon_or_object_used = models.CharField(max_length=255, blank=True, null=True, verbose_name="Type of Weapon or Object Used")
    DEGREE_OF_INJURY_CHOICES = [('HARM', 'Harm'), ('LESS_HARM', 'Less Harm'), ('GRIEVOUS_HARM', 'Grievous Harm')]
    immediate_degree_of_injury = models.CharField(max_length=20, choices=DEGREE_OF_INJURY_CHOICES, blank=True, null=True, verbose_name="Immediate Degree of Injury")
    details_of_specimen_collected = models.TextField(blank=True, null=True, verbose_name="Details of Specimen Collected")
      # Fields for PART IV: Sexual Assault Case
    # A. General
    sa_nature_of_complaint = models.TextField(blank=True, null=True, verbose_name="(i) Nature of Complaint")
    sa_estimated_age = models.CharField(max_length=50, blank=True, null=True, verbose_name="(ii) Estimated Age of Person Examined")
    # B. FEMALE
    sa_female_genitalia_injuries = models.TextField(blank=True, null=True, verbose_name="(i) Physical State/Injuries to Genitalia (Labia Majora/Minora, Vagina, Cervix, Anus, Penetration)")
    sa_female_infections_discharge_blood = models.TextField(blank=True, null=True, verbose_name="(ii) Venereal Infections, Discharge, Blood (Genitalia/Anus)")
    sa_female_specimens_collected = models.TextField(blank=True, null=True, verbose_name="(iii) Details of Specimen/Smears Collected (Pubic Hairs, Blood)")
    # C. MALE
    sa_male_genitalia_injuries = models.TextField(blank=True, null=True, verbose_name="(i) Physical State/Injuries to Genitalia (Anus, Penetration for Anal Intercourse)")
    sa_male_infections_discharge_blood = models.TextField(blank=True, null=True, verbose_name="(ii) Venereal Infections, Discharge (Anus/Penis)")
    sa_male_specimens_collected = models.TextField(blank=True, null=True, verbose_name="(iii) Details of Specimen/Smears Collected (Pubic Hair, Blood)")
    # Medical Practitioner Remarks for SA
    sa_practitioner_remarks = models.TextField(blank=True, null=True, verbose_name="Medical Practitioner Remarks")
    sa_practitioner_name = models.CharField(max_length=255, blank=True, null=True, verbose_name="Practitioner Name")
    sa_practitioner_qualification = models.CharField(max_length=255, blank=True, null=True, verbose_name="Practitioner Qualification")
    sa_practitioner_reg_no = models.CharField(max_length=100, blank=True, null=True, verbose_name="Practitioner Registration Number")
    sa_practitioner_date = models.DateField(blank=True, null=True, verbose_name="Practitioner Signature Date") # Changed to DateField
    sa_official_stamp_details = models.CharField(max_length=255, blank=True, null=True, verbose_name="Official Stamp Details (e.g., 'Stamped')")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Incident: {self.Incident_Type} - {self.Name_of_Patient[:30]}"

    
    def get_absolute_url(self):
        return reverse("core:detailIncident", args=[self.id])
    
    @property
    def is_acknowledged_by_police(self):
        return self.police_acknowledged_by is not None and self.status == self.INCIDENT_STATUS.ACKNOWLEDGED_BY_POLICE

    @property
    def is_approved_by_doctor(self):
        return self.doctor_approved_by is not None and self.status not in [self.INCIDENT_STATUS.SUBMITTED, self.INCIDENT_STATUS.PENDING_DOCTOR_APPROVAL, self.INCIDENT_STATUS.REJECTED_BY_DOCTOR]