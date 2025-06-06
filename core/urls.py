from django.urls import path

from core import views

app_name = 'core'

urlpatterns = [
    
    path('', views.index, name='index'),
    path('manage/incident/add/', views.AddIncidentView.as_view(), name="addIncident"),
    path('manage/incident/<int:pk>/delete/', views.IncidentDeleteView.as_view(), name="deleteIncident"),
    path('manage/incident/<int:pk>/detail', views.IncidentDetailView.as_view(), name="detailIncident"),
    path('manage/teams/all/', views.TeamsListView.as_view(), name="teamsList"),
    path('manage/teams/<int:pk>/detail/', views.TeamDetailView.as_view(), name="teamDetail"),
    path('incidents/manage/incident/<int:pk>/pdf/', views.render_incident_pdf, name='render_incident_pdf'), # New PDF URL

    # Police Station Management URLs
    path('manage/stations/', views.PoliceStationListView.as_view(), name='station_list'),
    path('manage/stations/add/', views.PoliceStationCreateView.as_view(), name='station_add'),
]