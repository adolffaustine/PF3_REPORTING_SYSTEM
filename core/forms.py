from django import forms

from .models import Incident, Team, TeamMember, Hospital # Corrected import path for models

class AddIncidentForm(forms.ModelForm):
    class Meta:
        model = Incident
        fields = [

            'title',
            'Name_of_Patient',
            'Date_of_Accident',
            'Date_of_Admission',
            'urgency',
            'triggered','resolved', # Removed 'acknowledged'
            'assigned_to', # assigned_to might be better handled separately or by specific roles
            'hospital',
            'description',
        ]


class AssignIncidentForm(forms.ModelForm):
    assign_incident = forms.BooleanField(widget=forms.HiddenInput)
    class Meta:
        model = Incident
        fields = ["assigned_to",]


class IncidentStatusUpdateForm(forms.ModelForm):
    status_update = forms.BooleanField(widget=forms.HiddenInput, initial=True)
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