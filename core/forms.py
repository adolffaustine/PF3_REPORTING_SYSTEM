from django import forms

from .models import Incident, Team, TeamMember, Hospital, PoliceStation # Added PoliceStation
from accounts.models import Profile # For querying police officers

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column, HTML

class AddIncidentForm(forms.ModelForm):
    class Meta:
           model = Incident
           fields = [
            # 'case_file_no', # Moved to police acknowledgement, auto-generated
            # 'police_station', # Moved to police acknowledgement
            'Incident_Type',
            'Name_of_Patient',
            'Date_of_Accident',
            'Date_of_Admission',
            'urgency',
            'hospital',
            'description',
            'triggered',
            'resolved',
            'assigned_to',
            'patient_file_no',
            'nature_of_complaint',
            'estimated_age',
            'general_physical_mental_examination',
            'medical_history',
            'condition_appearance_of_clothes',
            'guardian_name',
            'guardian_relationship',
            'approx_age_of_injury',
            'contact_details_for_police', # Added

            'treatment_received',
            'description_of_site_situation_depth_of_injury',
            'type_of_weapon_or_object_used',
            'immediate_degree_of_injury',
            'details_of_specimen_collected',
             # Part IV Fields
            'sa_nature_of_complaint',
            'sa_estimated_age',
            'sa_female_genitalia_injuries',
            'sa_female_infections_discharge_blood',
            'sa_female_specimens_collected',
            'sa_male_genitalia_injuries',
            'sa_male_infections_discharge_blood',
            'sa_male_specimens_collected',
            'sa_practitioner_remarks',
            'sa_practitioner_name',
            'sa_practitioner_qualification',
            'sa_practitioner_reg_no',
            'sa_practitioner_date',
            'sa_official_stamp_details',
        ]
        # ...
           widgets = {
            'Incident_Type': forms.TextInput(attrs={'class': 'form-control'}),
            'Name_of_Patient': forms.TextInput(attrs={'class': 'form-control'}),
            'Date_of_Accident': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}),
            'Date_of_Admission': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}),
            'urgency': forms.Select(attrs={'class': 'form-select'}),
            'hospital': forms.Select(attrs={'class': 'form-select'}),
            'description': forms.Textarea(attrs={'rows': 4, 'class': 'form-control'}),
            'assigned_to': forms.Select(attrs={'class': 'form-select'}),
            'patient_file_no': forms.TextInput(attrs={'class': 'form-control'}),
            'nature_of_complaint': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'estimated_age': forms.TextInput(attrs={'class': 'form-control'}),
            'general_physical_mental_examination': forms.Textarea(attrs={'rows': 4, 'class': 'form-control'}),
            'medical_history': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'condition_appearance_of_clothes': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'guardian_name': forms.TextInput(attrs={'class': 'form-control'}),
            'guardian_relationship': forms.TextInput(attrs={'class': 'form-control'}),
            'approx_age_of_injury': forms.TextInput(attrs={'class': 'form-control'}),
            'contact_details_for_police': forms.Textarea(attrs={'rows': 3, 'class': 'form-control', 'placeholder': 'e.g., Doctor Smith, Ward B, 07XXXXXXXX'}),

            'treatment_received': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'description_of_site_situation_depth_of_injury': forms.Textarea(attrs={'rows': 4, 'class': 'form-control'}),
            'type_of_weapon_or_object_used': forms.TextInput(attrs={'class': 'form-control'}),
            'immediate_degree_of_injury': forms.Select(attrs={'class': 'form-select'}),
            'details_of_specimen_collected': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            # Part IV Widgets
            'sa_nature_of_complaint': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'sa_estimated_age': forms.TextInput(attrs={'class': 'form-control'}),
            'sa_female_genitalia_injuries': forms.Textarea(attrs={'rows': 4, 'class': 'form-control'}),
            'sa_female_infections_discharge_blood': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'sa_female_specimens_collected': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'sa_male_genitalia_injuries': forms.Textarea(attrs={'rows': 4, 'class': 'form-control'}),
            'sa_male_infections_discharge_blood': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'sa_male_specimens_collected': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'sa_practitioner_remarks': forms.Textarea(attrs={'rows': 4, 'class': 'form-control'}),
            'sa_practitioner_name': forms.TextInput(attrs={'class': 'form-control'}),
            'sa_practitioner_qualification': forms.TextInput(attrs={'class': 'form-control'}),
            'sa_practitioner_reg_no': forms.TextInput(attrs={'class': 'form-control'}),
            'sa_practitioner_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'sa_official_stamp_details': forms.TextInput(attrs={'class': 'form-control'}),
            
        }
class PoliceAcknowledgeForm(forms.ModelForm):
    assigned_police_officer = forms.ModelChoiceField(
        queryset=Profile.objects.filter(role__role__iexact="Police"), # Or use user.is_staff if that's your primary police marker
        required=False, # Make it optional if not always assigned immediately
        label="Assign to Officer",
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    class Meta:
        model = Incident
        fields = ['police_station', 'police_comments', 'assigned_police_officer', 'contact_details_for_hospital'] # Added police_station
        # police_station will now be a ModelChoiceField
        widgets = {
            # 'police_station': forms.TextInput(attrs={'class': 'form-control'}), # Changed to ModelChoiceField
            'police_comments': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'contact_details_for_hospital': forms.Textarea(attrs={'rows': 3, 'class': 'form-control', 'placeholder': 'e.g., Officer Juma, Desk Sergeant, 07XXXXXXXX'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['police_station'] = forms.ModelChoiceField(
            queryset=PoliceStation.objects.all(),
            widget=forms.Select(attrs={'class': 'form-select'}))

class AssignIncidentForm(forms.ModelForm):
    assign_incident = forms.BooleanField(widget=forms.HiddenInput)
    class Meta:
        model = Incident
        fields = ["assigned_to",]


class IncidentStatusUpdateForm(forms.ModelForm):
    # status_update = forms.BooleanField(widget=forms.HiddenInput, initial=True)
    class Meta:
        model = Incident
        # This form is for Nurse/Doctor to update non-workflow critical flags.
        # The 'status' field will be handled by the view logic based on the 'resolved' flag.
        fields = ['triggered','resolved']


class UpdateTeamDetail(forms.ModelForm):
    update_detail = forms.BooleanField(widget=forms.HiddenInput, initial=True)
    class Meta:
        model = Team
        fields = [
            'team_name',
            'team_description',
            'on_call',
            'shift_date',
            'shift_end_date',
            'leader',
        ]



class AddNewTeamMember(forms.ModelForm):
    add_member = forms.BooleanField(widget=forms.HiddenInput, initial=True)
    class Meta:
        model = TeamMember
        fields = [
            'profile'
        ]
        labels = {
            'profile':'Member'
        }

class PoliceStationForm(forms.ModelForm):
    class Meta:
        model = PoliceStation
        fields = ['name', 'location_details', 'contact_phone', 'contact_email']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'location_details': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'contact_phone': forms.TextInput(attrs={'class': 'form-control'}),
            'contact_email': forms.EmailInput(attrs={'class': 'form-control'}),
        }