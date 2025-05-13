from django.urls import path 
from . import views

urlpatterns = [
    path('importenseignants/', views.import_enseignants, name='import_enseignants'),
    path('listeenseignants/', views.liste_enseignants, name='liste_enseignants'),
    path('importsessions/', views.import_sessions, name='import_sessions'),
    path('listesessions/', views.liste_sessions, name='liste_sessions'),
    path('importdevoirs/', views.import_devoirs, name='import_devoirs'),
    path('listdevoirs/', views.visualiser_devoirs, name='liste_devoirs'),
    path('rechercher-enseignant/', views.rechercher_enseignant_view, name='rechercher_enseignant'),
    path('datesessions/', views.get_unique_session_dates, name='dates_sessions'),
    path('createdisponibilite/', views.create_disponibilite, name='create_disponibilite'),


    path('listedisponibilites/', views.gestion_disponibilites, name='liste_disponibilites'),
    path('affecter-profs/', views.affecter_profs_aux_sessions, name='affecter_profs'),
    path('generer-pdf/', views.generer_pdf_affectations, name='generer_pdf'),
    path('liste-affectations/', views.liste_affectations, name='liste_affectations'),
    path('count-responsables/', views.count_responsables_view, name='count-responsables'),
    path('enseignants-total-inferieur-surveillance/', views.enseignants_total_inferieur_surveillance_view, name='enseignants_total_inferieur_surveillance'),



]
