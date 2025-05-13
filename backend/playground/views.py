from django.shortcuts import render
from django.http import HttpResponse
import os
from django.shortcuts import render, redirect
from django.conf import settings
from django.contrib import messages
from openpyxl import load_workbook
import pandas as pd

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from openpyxl import load_workbook
import json
 
from .models import Disponibilite, Enseignant, Session, Devoir
# Create your views here.
# request handler 


@csrf_exempt
def import_enseignants(request):
    if request.method == 'POST' and request.FILES.get('fichier_excel'):
        try:
            # Charger le fichier Excel
            df = pd.read_excel(request.FILES['fichier_excel'])
            
            # Remplacer les valeurs NaN par des valeurs par défaut
            df = df.fillna({
                'TD': 0,
                'TP': 0,
                'coef': 1.0,
                'Nombre de Séances de surveillance': 0
            })
            
            # Convertir les colonnes numériques
            df['TD'] = pd.to_numeric(df['TD'], errors='coerce').fillna(0)
            df['TP'] = pd.to_numeric(df['TP'], errors='coerce').fillna(0)
            df['coef'] = pd.to_numeric(df['coef'], errors='coerce').fillna(1.0)
            df['Nombre de Séances de surveillance'] = pd.to_numeric(
                df['Nombre de Séances de surveillance'], 
                errors='coerce'
            ).fillna(0)
            
            enseignants_crees = 0
            enseignants_mis_a_jour = 0
            
            for _, row in df.iterrows():
                # Vérifier si l'Enseignant existe déjà
                nom_prenom = row['Nom Et Prénom Enseignant']
                departement = row['Département']
                grade = row['Grade']
                
                enseignant, created = Enseignant.objects.get_or_create(
                    nom_prenom=nom_prenom,
                    departement=departement,
                    grade=grade,
                    defaults={
                        'cours': row['Cours'],
                        'heures_td': int(row['TD']),
                        'heures_tp': int(row['TP']),
                        'coefficient': float(row['coef']),
                        'seances_surveillance': int(row['Nombre de Séances de surveillance']),
                        'total_S': 0,  # Initialisé à zéro
                        'total_RS': 0,  # Initialisé à zéro
                        'total_R': 0,  # Initialisé à zéro
                        'total': 0  # Initialisé à zéro
                    }
                )
                
                if not created:
                    # Mettre à jour l'enseignant existant
                    enseignant.cours = row['Cours']
                    enseignant.heures_td = int(row['TD'])
                    enseignant.heures_tp = int(row['TP'])
                    enseignant.coefficient = float(row['coef'])
                    enseignant.seances_surveillance = int(row['Nombre de Séances de surveillance'])
                    enseignant.save()
                    enseignants_mis_a_jour += 1
                else:
                    enseignants_crees += 1
            
            return JsonResponse({
                'status': 'success',
                'enseignants_importes': enseignants_crees,
                'enseignants_mis_a_jour': enseignants_mis_a_jour,
                'total_lignes': len(df)
            })
            
        except Exception as e:
            return JsonResponse({
                'status': 'error',
                'message': str(e),
                'solution': 'Vérifiez que toutes les colonnes numériques contiennent des valeurs valides'
            }, status=500)
    
    return JsonResponse({'error': 'Requête invalide'}, status=400)

def liste_enseignants(request):
    try:
        
        # Récupération avec sélection des champs pertinents
        enseignants = Enseignant.objects.all().values(
            'id',
            'nom_prenom',
            'departement',
            'grade',
            'cours',
            'heures_td',
            'heures_tp',
            'coefficient',
            'seances_surveillance',
            'total_R',
            'total_RS',
            'total_S' 
            
        )
        
        # Conversion en liste pour JsonResponse
        data = list(enseignants)
        
        return JsonResponse({
            'status': 'success',
            'count': len(data),
            'enseignants': data
        })
        
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        }, status=500)

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import pandas as pd
from .models import Session  # Remplacez 'myapp' par le nom de votre application

@csrf_exempt
def import_sessions(request):
    if request.method == 'POST' and request.FILES.get('fichier_excel'):
        try:
            # Charger le fichier Excel
            df = pd.read_excel(request.FILES['fichier_excel'])
            
           
            
            # Initialisation des compteurs
            sessions_crees = 0
            sessions_mises_a_jour = 0
            
            for _, row in df.iterrows():
                # Extraire les données de la ligne
                session_id = row['session_id']
                
                date = row['date']
                seance = row['seance']
                nb_salle = min(max(int(row.get('nb_salle', 20)), 20), 50)  # Entre 20 et 50
                
                # Créer ou mettre à jour la session
                session, created = Session.objects.get_or_create(
                    session_id=session_id,
                    defaults={
                        'date': date,
                        'seance': seance,
                        'nb_salle': nb_salle,
                        'nb_prof_aff': 0 # Valeur par défaut
                    }
                )
                
                if not created:
                    # Mettre à jour les champs existants si nécessaire
                    session.date = date
                    session.seance = seance
                    session.nb_salle = nb_salle
                    session.save()
                    sessions_mises_a_jour += 1
                else:
                    sessions_crees += 1
            
            return JsonResponse({
                'status': 'success',
                'sessions_importees': sessions_crees,
                'sessions_mises_a_jour': sessions_mises_a_jour
            })
            
        except Exception as e:
            return JsonResponse({
                'status': 'error',
                'message': str(e)
            }, status=500)
    
    return JsonResponse({'error': 'Requête invalide'}, status=400)

def liste_sessions(request):
    try:
        sessions = Session.objects.all().values(
            'id',
            'session_id',
            'date',
            'seance',
            'nb_salle',
            'nb_prof_aff'
            
        )
        
        # Conversion pour inclure l'affichage de la séance
        data = []
        for s in sessions:
            session_data = s
            session_data['seance_display'] = dict(Session.SEANCE_CHOICES).get(s['seance'])
            data.append(session_data)
        
        return JsonResponse({
            'status': 'success',
            'count': len(data),
            'sessions': data
        })
        
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        }, status=500)
    



@csrf_exempt
def import_devoirs(request):
    if request.method == 'POST' and request.FILES.get('fichier_excel'):
        try:
            # Charger le fichier Excel
            df = pd.read_excel(request.FILES['fichier_excel'])

            # Vérifier les colonnes attendues
            required_columns = {'session_id', 'matiere', 'profResponsable'}
            if not required_columns.issubset(df.columns):
                return JsonResponse({
                    'status': 'error',
                    'message': f"Colonnes manquantes. Attendues : {required_columns}, reçues : {list(df.columns)}"
                }, status=400)

            # Initialisation des compteurs
            devoirs_crees = 0
            erreurs = []

            for _, row in df.iterrows():
                try:
                    session_id = row['session_id']
                    matiere = row['matiere']
                    profResponsable_nom = row['profResponsable']

                    # Vérifier si l'enseignant existe, sinon le créer
                    enseignant, created = Enseignant.objects.get_or_create(nom_prenom=profResponsable_nom)

                    # Vérifier si la session existe
                    try:
                        session = Session.objects.get(session_id=session_id)
                    except Session.DoesNotExist:
                        erreurs.append(f"Session {session_id} non trouvée. Ignorée.")
                        continue

                    # Créer un devoir
                    Devoir.objects.create(
                        matiere=matiere,
                        profResponsable=enseignant.nom_prenom,
                        session=session
                    )
                    devoirs_crees += 1

                except Exception as e:
                    erreurs.append(f"Erreur lors du traitement de la ligne {row.get('session_id', 'inconnue')} : {str(e)}")

            # Retourner la réponse JSON
            return JsonResponse({
                'status': 'success',
                'devoirs_importes': devoirs_crees,
                'erreurs': erreurs
            })

        except Exception as e:
            # Capturer les erreurs globales
            return JsonResponse({
                'status': 'error',
                'message': f"Une erreur s'est produite : {str(e)}"
            }, status=500)

    return JsonResponse({'error': 'Requête invalide'}, status=400)




@csrf_exempt
def visualiser_devoirs(request):
    if request.method == 'GET':
        try:
            # Récupérer tous les devoirs depuis la base de données
            devoirs = Devoir.objects.all()

            # Formater les données des devoirs pour la réponse JSON
            data = []
            for devoir in devoirs:
                data.append({
                    'id': devoir.id,
                    'matiere': devoir.matiere,
                    'profResponsable': devoir.profResponsable,
                    'session_id': devoir.session.session_id,  # Accéder à la session associée
                })

            # Retourner les données au format JSON
            return JsonResponse({
                'status': 'success',
                'devoirs': data
            })

        except Exception as e:
            # Capturer les erreurs globales
            return JsonResponse({
                'status': 'error',
                'message': f"Une erreur s'est produite : {str(e)}"
            }, status=500)

    return JsonResponse({'error': 'Requête invalide'}, status=400)



from django.http import JsonResponse
from django.views.decorators.http import require_GET
from .models import Enseignant

@require_GET
def rechercher_enseignant_view(request):
    """
    Vue pour rechercher des enseignants par leur nom.
    Exemple d'URL : /api/rechercher-enseignant/?nom=Doe
    """
    # Récupérer le paramètre de recherche depuis les chaînes de requête
    nom_recherche = request.GET.get('nom', '').strip()

    if not nom_recherche:
        return JsonResponse({"erreur": "Le paramètre 'nom' est requis."}, status=400)

    # Rechercher les enseignants correspondants
    enseignants = Enseignant.rechercher_par_nom(nom_recherche)

    # Formater les résultats en JSON
    data = list(enseignants.values(
        "id",
        "nom_prenom",
        "departement",
        "grade",
        "cours",
        "heures_td",
        "heures_tp",
        "coefficient",
        "seances_surveillance"
    ))

    return JsonResponse(data, safe=False) 

@csrf_exempt  # Temporaire pour les tests Postman
def gestion_disponibilites(request):
    try:
        # Récupère toutes les entrées de disponibilité avec les enseignants associés
        toutes_dispos = Disponibilite.objects.all().select_related('enseignant')
        
        # Formatage des données
        resultats = []
        for dispo in toutes_dispos:
            resultats.append({
                'professeur': dispo.enseignant.nom_prenom,
                'departement': dispo.enseignant.departement,
                'indisponibilites': dispo.indisponibilites  # Liste brute des créneaux indisponibles
            })
        
        return JsonResponse({
            'status': 'success',
            'count': len(resultats),
            'disponibilites': resultats
        })
    
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        }, status=500)
from django.db.models import Q, F
from django.http import JsonResponse
from .models import Enseignant, Session, Affectation, Devoir



from django.db.models import F, Q
from collections import defaultdict
from django.http import JsonResponse

def is_enseignant_disponible(enseignant, session):
    """
    Vérifie si un enseignant est disponible pour une session donnée.
    """
    try:
        disponibilite = Disponibilite.objects.get(enseignant=enseignant)
        for indisponibilite in disponibilite.indisponibilites:
            if (
                indisponibilite['date'] == str(session.date) and
                indisponibilite['seance'] == session.seance
            ):
                return False  # Indisponible pour cette session
        return True  # Disponible
    except Disponibilite.DoesNotExist:
        return True  # Pas d'indisponibilités enregistrées, donc disponible

def create_aff(session, enseignant_responsable, role):
    """Créer une nouvelle affectation."""
    Affectation.objects.create(
        session=session,
        enseignant=enseignant_responsable,
        role=role
    )

def affecter_profs_aux_sessions(request):
    # Étape 0 : Réinitialisation des données
    Affectation.objects.all().delete()
    Enseignant.objects.all().update(
        total_S=0,
        total_RS=0,
        total_R=0,
        total=0
    )
    Session.objects.all().update(
        nb_prof_aff=0
    )
    # Étape 1 : Récupérer tous les jours uniques où des sessions sont programmées
    jours_uniques = Session.objects.values_list('date', flat=True).distinct().order_by('date')
    # Étape 2 : Affecter les profs responsables aux sessions
    for jour in jours_uniques:
        sessions_du_jour = Session.objects.filter(date=jour).order_by('seance')
        for session in sessions_du_jour:
            # Récupérer tous les devoirs de la session
            devoirs = Devoir.objects.filter(session=session)
            for devoir in devoirs:
                try:
                    enseignant_responsable = Enseignant.objects.get(nom_prenom=devoir.profResponsable)
                except Enseignant.DoesNotExist:
                    continue  # Passer si aucun enseignant n'est trouvé
                # Déterminer le rôle de l'enseignant responsable
                if enseignant_responsable.seances_surveillance == 0:
                    role = 'R'
                else:
                    role = 'RS'
                # Vérifier si une affectation existe déjà pour cet enseignant et cette session
                if not Affectation.objects.filter(session=session, enseignant=enseignant_responsable).exists():
                    create_aff(session, enseignant_responsable, role)
                    # Mettre à jour les champs de l'enseignant
                    if role == 'R':
                        enseignant_responsable.total_R += 1
                    elif role == 'RS':
                        enseignant_responsable.total_RS += 1
                        session.nb_prof_aff += 1
                        enseignant_responsable.total += 1
                    enseignant_responsable.save()
                    session.save()

    # Étape 3 : Affecter des surveillants supplémentaires
    for jour_index, jour in enumerate(jours_uniques):
        sessions_du_jour = Session.objects.filter(date=jour).order_by('seance')
        for session in sessions_du_jour:
            # Calculer le nombre de surveillants nécessaires
            surveillants_necessaires = session.nb_salle * 2 - session.nb_prof_aff
            if surveillants_necessaires > 0:
                # Étape 3.1 : Trouver des enseignants déjà affectés ce jour-là
                enseignants_deja_affectes = Enseignant.objects.filter(
                    seances_surveillance__gt=0,          # Quota valide
                    total__lt=F('seances_surveillance'),  # Quota non atteint
                    affectations__session__date=jour     # Déjà affectés ce jour-là
                ).exclude(
                    Q(affectations__session__date=jour) & Q(affectations__session__seance=session.seance)
                ).order_by('total')
                # Affecter les enseignants déjà affectés
                for enseignant in enseignants_deja_affectes[:surveillants_necessaires]:
                    if (
                        not Affectation.objects.filter(session=session, enseignant=enseignant).exists() and
                        is_enseignant_disponible(enseignant, session)
                    ):
                        create_aff(session, enseignant, role='S')
                        # Mettre à jour les champs de l'enseignant
                        enseignant.total_S += 1
                        enseignant.total += 1
                        enseignant.save()
                        # Mettre à jour le nombre de profs affectés à la session
                        session.nb_prof_aff += 1
                        session.save()
                        # Décrémenter le nombre de surveillants nécessaires
                        surveillants_necessaires -= 1
                        if surveillants_necessaires == 0:
                            break

                # Étape 3.2 : Trouver des enseignants responsables le jour suivant
                if surveillants_necessaires > 0 and jour_index + 1 < len(jours_uniques):
                    jour_suivant = jours_uniques[jour_index + 1]
                    sessions_jour_suivant = Session.objects.filter(date=jour_suivant)
                    # Récupérer tous les profs responsables des devoirs associés aux sessions du jour suivant
                    devoirs_jour_suivant = Devoir.objects.filter(session__in=sessions_jour_suivant)
                    profs_responsables_jour_suivant = [d.profResponsable for d in devoirs_jour_suivant]
                    # Identifier les enseignants responsables du jour suivant
                    enseignants_jour_suivant = Enseignant.objects.filter(
                        nom_prenom__in=profs_responsables_jour_suivant,
                        seances_surveillance__gt=0,           # Quota valide
                        total__lt=F('seances_surveillance'),  # Quota non atteint
                    ).exclude(
                        Q(affectations__session__date=jour) & Q(affectations__session__seance=session.seance)
                    ).order_by('total')
                    # Affecter les enseignants responsables le jour suivant
                    for enseignant in enseignants_jour_suivant[:surveillants_necessaires]:
                        if (
                            not Affectation.objects.filter(session=session, enseignant=enseignant).exists() and
                            is_enseignant_disponible(enseignant, session)
                        ):
                            create_aff(session, enseignant, role='S')
                            # Mettre à jour les champs de l'enseignant
                            enseignant.total_S += 1
                            enseignant.total += 1
                            enseignant.save()
                            # Mettre à jour le nombre de profs affectés à la session
                            session.nb_prof_aff += 1
                            session.save()
                            # Décrémenter le nombre de surveillants nécessaires
                            surveillants_necessaires -= 1
                            if surveillants_necessaires == 0:
                                break

                # Étape 3.3 : Trouver des enseignants responsables le jour après le suivant
                if surveillants_necessaires > 0 and jour_index + 2 < len(jours_uniques):
                    jour_apres_suivant = jours_uniques[jour_index + 2]
                    sessions_jour_apres_suivant = Session.objects.filter(date=jour_apres_suivant)
                    # Récupérer tous les profs responsables des devoirs associés aux sessions du jour après le suivant
                    devoirs_jour_apres_suivant = Devoir.objects.filter(session__in=sessions_jour_apres_suivant)
                    profs_responsables_jour_apres_suivant = [d.profResponsable for d in devoirs_jour_apres_suivant]
                    # Identifier les enseignants responsables du jour après le suivant
                    enseignants_jour_apres_suivant = Enseignant.objects.filter(
                        nom_prenom__in=profs_responsables_jour_apres_suivant,
                        seances_surveillance__gt=0,           # Quota valide
                        total__lt=F('seances_surveillance'),  # Quota non atteint
                    ).exclude(
                        Q(affectations__session__date=jour) & Q(affectations__session__seance=session.seance)
                    ).order_by('total')
                    # Affecter les enseignants responsables le jour après le suivant
                    for enseignant in enseignants_jour_apres_suivant[:surveillants_necessaires]:
                        if (
                            not Affectation.objects.filter(session=session, enseignant=enseignant).exists() and
                            is_enseignant_disponible(enseignant, session)
                        ):
                            create_aff(session, enseignant, role='S')
                            # Mettre à jour les champs de l'enseignant
                            enseignant.total_S += 1
                            enseignant.total += 1
                            enseignant.save()
                            # Mettre à jour le nombre de profs affectés à la session
                            session.nb_prof_aff += 1
                            session.save()
                            # Décrémenter le nombre de surveillants nécessaires
                            surveillants_necessaires -= 1
                            if surveillants_necessaires == 0:
                                break

    # Étape 4 : Maximiser les charges des enseignants
    enseignants_eligibles = Enseignant.objects.filter(total__lt=F('seances_surveillance'))
    affectations_par_enseignant = defaultdict(list)
    # Stocker les jours et sessions où chaque enseignant est déjà affecté
    for aff in Affectation.objects.select_related('session', 'enseignant'):
        affectations_par_enseignant[aff.enseignant].append(aff.session.date)
    # Identifier les sessions ayant encore besoin de surveillants
    sessions_prioritaires = Session.objects.annotate(
        surveillants_restants=(F('nb_salle') * 2) - F('nb_prof_aff')
    ).filter(surveillants_restants__gt=0).order_by('-surveillants_restants')
    # Essayer de compléter les quotas des enseignants
    for enseignant in enseignants_eligibles:
        jours_affectes = set(affectations_par_enseignant[enseignant])
        jours_disponibles = sorted(set(jours_uniques) - jours_affectes)
        # Prioriser les jours où l'enseignant est déjà affecté
        for jour in sorted(jours_affectes):
            sessions_du_jour = sessions_prioritaires.filter(date=jour).exclude(
                affectations__enseignant=enseignant
            ).order_by('-surveillants_restants')
            for session in sessions_du_jour:
                if enseignant.total >= enseignant.seances_surveillance:
                    break  # Arrêter si le quota est atteint
                if session.nb_prof_aff >= session.nb_salle * 2:
                    continue  # Passer si la session a atteint son quota
                if (
                    not Affectation.objects.filter(session=session, enseignant=enseignant).exists() and
                    is_enseignant_disponible(enseignant, session)
                ):
                    create_aff(session, enseignant, role='S')
                    # Mettre à jour les champs de l'enseignant
                    enseignant.total_S += 1
                    enseignant.total += 1
                    enseignant.save()
                    # Mettre à jour le nombre de profs affectés à la session
                    session.nb_prof_aff += 1
                    session.save()
        # Si le quota n'est toujours pas atteint, passer aux jours disponibles
        for jour in jours_disponibles:
            sessions_du_jour = sessions_prioritaires.filter(date=jour).exclude(
                affectations__enseignant=enseignant
            ).order_by('-surveillants_restants')
            for session in sessions_du_jour:
                if enseignant.total >= enseignant.seances_surveillance:
                    break  # Arrêter si le quota est atteint
                if session.nb_prof_aff >= session.nb_salle * 2:
                    continue  # Passer si la session a atteint son quota
                if (
                    not Affectation.objects.filter(session=session, enseignant=enseignant).exists() and
                    is_enseignant_disponible(enseignant, session)
                ):
                    create_aff(session, enseignant, role='S')
                    # Mettre à jour les champs de l'enseignant
                    enseignant.total_S += 1
                    enseignant.total += 1
                    enseignant.save()
                    # Mettre à jour le nombre de profs affectés à la session
                    session.nb_prof_aff += 1
                    session.save()

    return JsonResponse({"message": "Affectations terminées avec succès."})

#*---------------------------------------------------------------------------------------*/

from django.http import HttpResponse
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from .models import Enseignant, Affectation

def generer_pdf_affectations(request):
    # Créer une réponse HTTP avec le type de contenu PDF
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="affectations_enseignants.pdf"'

    # Créer un objet PDF
    p = canvas.Canvas(response, pagesize=letter)
    width, height = letter  # Dimensions de la page (612x792 points)

    # Titre du document
    p.setFont("Helvetica-Bold", 16)
    p.drawString(50, height - 50, "Affectations des Enseignants")

    # Position initiale pour écrire le contenu
    y_position = height - 100

    # Récupérer tous les enseignants
    enseignants = Enseignant.objects.all()

    for enseignant in enseignants:
        # Récupérer les affectations pour cet enseignant
        affectations = Affectation.objects.filter(enseignant=enseignant).order_by('enseignant__nom_prenom')

        if affectations.exists():
            # Écrire le nom de l'enseignant
            p.setFont("Helvetica-Bold", 12)
            p.drawString(50, y_position, f"{enseignant.nom_prenom} ({enseignant.total} /  {enseignant.seances_surveillance})")
            y_position -= 20

            # Écrire les détails des affectations
            p.setFont("Helvetica", 10)
            for affectation in affectations:
                session = affectation.session
                p.drawString(70, y_position, f"- Date: {session.date}, Séance: {session.seance}, Rôle: {affectation.role}")
                y_position -= 15

            # Ajouter une ligne vide entre les enseignants
            y_position -= 10

        # Vérifier si nous devons passer à une nouvelle page
        if y_position < 50:
            p.showPage()  # Nouvelle page
            y_position = height - 50  # Réinitialiser la position Y

    # Sauvegarder le PDF
    p.save()

    return response 





def liste_affectations(request):
    # Récupérer toutes les affectations avec les relations préchargées pour optimiser les requêtes
    affectations = Affectation.objects.all().select_related('session', 'enseignant')

    # Formater les données pour la réponse JSON
    data = [
        {
            "session": str(affectation.session),  # Convertir l'objet Session en chaîne (utilise __str__)
            "enseignant": str(affectation.enseignant),  # Convertir l'objet Enseignant en chaîne (utilise __str__)
            "role": affectation.role,  # Rôle de l'affectation (R, RS, ou S)
        }
        for affectation in affectations
    ]

    # Retourner les données sous forme de réponse JSON
    return JsonResponse(data, safe=False)







def count_responsables_view(request):
    if request.method == 'GET':
        # Récupérer tous les noms uniques de profResponsable dans le modèle Devoir
        responsables_uniques = Devoir.objects.values_list('profResponsable', flat=True).distinct()

        # Filtrer les profs qui existent dans le modèle Enseignant
        enseignants_valides = Enseignant.objects.filter(nom_prenom__in=responsables_uniques)

        # Compter les enseignants valides
        count = enseignants_valides.count()

        return JsonResponse({"nombre_responsables": count})
    




    from django.http import JsonResponse
from .models import Enseignant

def enseignants_total_inferieur_surveillance_view(request):
    """
    Vue qui retourne la liste des enseignants dont le total est inférieur au nombre de séances de surveillance.
    """
    enseignants = Enseignant.enseignants_total_inferieur_surveillance()
    data = list(enseignants.values(
        "id",
        "nom_prenom",
        "departement",
        "grade",
        "total",
        "seances_surveillance"
    ))
    return JsonResponse(data, safe=False)

def get_unique_session_dates(request):
    # Fetch all sessions and extract unique dates using a set
    sessions = Session.objects.all()
    unique_dates = set(session.date for session in sessions)
    
    # Convert the set to a sorted list (optional, if you want sorted dates)
    unique_dates_list = sorted(unique_dates)
    
    # Return the unique dates as a JSON response
    return JsonResponse({'dates': unique_dates_list})


from django.core.exceptions import ObjectDoesNotExist


@csrf_exempt
def create_disponibilite(request):
    if request.method == 'POST':
        try:
            # Parse the JSON data from the request body
            data = json.loads(request.body)
            
            # Extract enseignant name, date, and seance from the request data
            enseignant_name = data.get('enseignant_name')
            dates = data.get('date')
            seances = data.get('seance')
            
            # Validate that all required fields are provided
            if not enseignant_name or not dates or not seances:
                return JsonResponse({'error': 'enseignant_name, date, and seance are required'}, status=400)
            
            # Convert enseignant_name to uppercase for case-insensitive matching
            enseignant_name_upper = enseignant_name.upper()
            
            # Fetch the Enseignant instance by name (case-insensitive)
            try:
                enseignant = Enseignant.objects.get(nom_prenom__iexact=enseignant_name)
            except ObjectDoesNotExist:
                return JsonResponse({'error': 'Enseignant not found'}, status=404)
            
            # Get or create the Disponibilite instance for the enseignant
            disponibilite, created = Disponibilite.objects.get_or_create(enseignant=enseignant)
            
            # Add the new indisponibilite to the existing list (if not already present)
            new_indisponibilite = {dates: seances}
            if new_indisponibilite not in disponibilite.indisponibilites:
                disponibilite.indisponibilites.append(new_indisponibilite)
                disponibilite.save()
            
            # Return a success response
            return JsonResponse({
                'message': 'Indisponibilité ajoutée avec succès',
                
                'enseignant': str(disponibilite.enseignant),
                'indisponibilites': disponibilite.indisponibilites
            }, status=201 if created else 200)
        
        except Exception as e:
            # Handle any unexpected errors
            return JsonResponse({'error': str(e)}, status=500)
    
    # Return an error if the request method is not POST
    return JsonResponse({'error': 'Only POST requests are allowed'}, status=405)