from django.shortcuts import render, get_object_or_404, redirect

from django.urls import reverse_lazy

from django.views import View
from django.views.generic.edit import CreateView
from django.views.generic import ListView, DetailView, DeleteView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin # For class-based views
from django.utils import timezone
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin

from core.models import Incident, Team
from core.forms import (
    AddIncidentForm,
    AssignIncidentForm, 
    IncidentStatusUpdateForm,
    UpdateTeamDetail,
    AddNewTeamMember,
)
from django.contrib.auth.decorators import login_required
# Create your views here.
@login_required
def index(request):
    incidents = Incident.objects.all()
    context = {
        "incidents":incidents,
    }
    return render(request, "index.html", context)


class IncidentDetailView(LoginRequiredMixin, View):
    template_name = 'manage/incidents/detail_incident.html'
    def get(self,request, *args, **kwargs):
        incident = get_object_or_404(Incident, id=self.kwargs['pk'])
        assign_incident_form = AssignIncidentForm(instance=incident)
        update_status_form = IncidentStatusUpdateForm(instance=incident)
        user_profile = request.user.profile if hasattr(request.user, 'profile') else None

        context = {
            'incident':incident,
            'assign_incident_form':assign_incident_form,
            'update_status_form':update_status_form,
            'user_profile': user_profile,
        }
        
        return render(request, self.template_name, context)
    
    def post(self, request, *args, **kwargs):
        incident = get_object_or_404(Incident, id=self.kwargs['pk'])
        user_profile = request.user.profile if hasattr(request.user, 'profile') else None

        # Doctor Approval Action
        if "doctor_approve" in request.POST and user_profile and user_profile.is_doctor:
            if incident.status == Incident.INCIDENT_STATUS.PENDING_DOCTOR_APPROVAL:
                incident.approved_by_doctor = user_profile
                incident.doctor_approval_date = timezone.now()
                incident.status = Incident.INCIDENT_STATUS.PENDING_POLICE_ACKNOWLEDGEMENT
                incident.doctor_comments = request.POST.get('doctor_comments', '')
                incident.save()
                messages.success(request, "Incident approved by Doctor and sent for Police acknowledgement.")
            else:
                messages.error(request, "Incident is not pending Doctor approval or you are not authorized.")
            return redirect("core:detailIncident", pk=incident.pk)

        # Police Acknowledgement Action
        if "police_acknowledge" in request.POST and user_profile and user_profile.is_police:
            if incident.status == Incident.INCIDENT_STATUS.PENDING_POLICE_ACKNOWLEDGEMENT:
                incident.police_acknowledged_by = user_profile
                incident.police_acknowledgement_date = timezone.now()
                incident.status = Incident.INCIDENT_STATUS.ACKNOWLEDGED_BY_POLICE
                incident.police_comments = request.POST.get('police_comments', '')
                # incident.acknowledged = True # If you still have this field and want to use it
                incident.save()
                messages.success(request, "Incident acknowledged by Police.")
            else:
                messages.error(request, "Incident is not pending Police acknowledgement or you are not authorized.")
            return redirect("core:detailIncident", pk=incident.pk)

        # Fallback for existing forms if they are still used independently
        assign_incident_form = AssignIncidentForm(request.POST or None, instance=incident)
        update_status_form = IncidentStatusUpdateForm(request.POST or None, instance=incident) # Be cautious with this form

        if "assign_incident" in request.POST:
            # assign_incident_form = AssignIncidentForm(request.POST, instance=incident)
            if assign_incident_form.is_valid():
                assign_incident_form.save()
                messages.success(request, "Successfully assigned incident to the team")
                return redirect("core:detailIncident", pk=incident.pk)
        if "status_update" in request.POST:
            if update_status_form.is_valid():
               # Save the form but don't commit to DB immediately
                # This allows us to modify the instance before the final save
                incident_instance = update_status_form.save(commit=False)
                
                # If the 'resolved' flag was set to True by the form
                if incident_instance.resolved:
                    incident_instance.status = Incident.INCIDENT_STATUS.RESOLVED
                
                incident_instance.save() # Now save the instance with any changes
                messages.success(request, "Incident flags and status successfully updated.")
                return redirect("core:detailIncident", pk=incident.pk)
            else:
                messages.error(request, f"Error updating flags: {update_status_form.errors}")
        context = {
            'incident':incident,
            'assign_incident_form':assign_incident_form,
            'update_status_form':update_status_form,
            'user_profile': user_profile,
        }
        return render(request, self.template_name, context)


class AddIncidentView(SuccessMessageMixin,CreateView):
    form_class = AddIncidentForm
    template_name = "manage/incidents/add_incident.html"
    success_message = "Incident Reported"
    success_url = reverse_lazy("core:index")

    def form_valid(self, form):
        if self.request.user.is_authenticated and hasattr(self.request.user, 'profile'):
            form.instance.reported_by = self.request.user.profile
            # Set initial status based on reporter's role
            if self.request.user.profile.is_nurse:
                form.instance.status = Incident.INCIDENT_STATUS.PENDING_DOCTOR_APPROVAL
            else: # Victim or other staff not explicitly a nurse
                form.instance.status = Incident.INCIDENT_STATUS.PENDING_POLICE_ACKNOWLEDGEMENT
            form.instance.save()
        elif self.request.user.is_authenticated: # User has no profile, fallback or error
            messages.error(self.request, "User profile not found. Cannot report incident.")
            return self.form_invalid(form)
        return super().form_valid(form)

class IncidentDeleteView(SuccessMessageMixin, DeleteView):
    model = Incident
    template_name = "manage/incidents/delete_incident.html"
    success_url = reverse_lazy("core:index")
    success_message = "Incident Deleted Successfully"


class TeamsListView(ListView):
    model = Team
    template_name = "manage/teams/team_list.html"
    context_object_name = 'teams'


class TeamDetailView(View):
    template_name = "manage/teams/team_detail.html"
    def get(self, request, *args, **kwargs):
        team = get_object_or_404(Team, id=self.kwargs['pk'])
        update_detail = UpdateTeamDetail(instance=team)
        add_member = AddNewTeamMember()
        context = {
            'team':team,
            'update_detail':update_detail,
            'add_member':add_member,
        }
        return render(request, self.template_name, context)
    def post(self, request, *args, **kwargs):
        team = get_object_or_404(Team, id=self.kwargs['pk'])
        update_detail = UpdateTeamDetail(instance=team)
        add_member = AddNewTeamMember()
        if 'update_detail' in request.POST:
            update_detail = UpdateTeamDetail(request.POST, instance=team)
            if update_detail.is_valid():
                update_detail.save()
                messages.success(request, "Team Detail Updated Successfully")
                return redirect('core:teamDetail', pk=team.pk)
        if 'add_member' in request.POST:
            add_member = AddNewTeamMember(request.POST)
            if add_member.is_valid():
                add_member.save(commit=False)
                add_member.instance.team = team
                add_member.save()
                messages.success(request, "New Member added into the Team")
                return redirect("core:teamDetail", pk=team.pk)
        context = {
            'team':team,
            'update_detail':update_detail,
            'add_member':add_member,
        }
        return render(request, self.template_name, context)