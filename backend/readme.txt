ceci est mon fichier models.py :
# Create your models here.
from django.db import models

class Enseignant(models.Model):
    # Champs existants
    nom_prenom = models.CharField(max_length=200, verbose_name="Nom et Prénom")
    departement = models.CharField(max_length=100)
    grade = models.CharField(max_length=100, verbose_name="Grade")  # Grade sans liste de choix
    cours = models.CharField(max_length=200)
    heures_td = models.IntegerField(default=0, verbose_name="Heures TD")
    heures_tp = models.IntegerField(default=0, verbose_name="Heures TP")
    coefficient = models.FloatField(default=1.0)
    seances_surveillance = models.PositiveIntegerField(default=0)

    # Nouveaux champs
    total_S = models.IntegerField(default=0, verbose_name="Total Surveillance")
    total_RS = models.IntegerField(default=0, verbose_name="Total Responsabilité de Surveillance")
    total_R = models.IntegerField(default=0, verbose_name="Total Responsabilité")
    total = models.IntegerField(default=0, verbose_name="Total Général")

    class Meta:
        verbose_name = "Enseignant"
        verbose_name_plural = "Enseignants"
        ordering = ['nom_prenom']

    def __str__(self):
        return f"{self.nom_prenom} - {self.departement}"

    @property
    def volume_horaire_total(self):
        return self.heures_td + self.heures_tp

    def calculer_total(self):
        """Méthode pour calculer et mettre à jour le champ 'total'."""
        self.total = self.total_S + self.total_RS 
class Session(models.Model):
    SEANCE_CHOICES = [
        ('s1', '08:30-10:00'),
        ('s2', '10:45-12:15'), 
        ('s3', '13:00-14:30'),
        ('s4', '15:15-16:45'),
    ]
    
    session_id = models.CharField(max_length=10)
    date = models.DateField()
    nb_salle= models.IntegerField(2)
    seance = models.CharField(
    max_length=2, 
    choices=SEANCE_CHOICES,
    default='s1' )
    nb_prof_aff = models.IntegerField(default=1.0)  

    def __str__(self):
        return f"{self.session_id} - {self.date} {self.seance}"



class Affectation(models.Model):
    session = models.ForeignKey(
        Session,
        on_delete=models.CASCADE,
        related_name='affectations',
        verbose_name="Session d'Examen"
    )
    enseignant = models.ForeignKey(
        Enseignant,
        on_delete=models.CASCADE,
        related_name='affectations',
        verbose_name="Enseignant"
    )
    role = models.CharField(
        max_length=2,  # Réduit la taille car les valeurs sont plus courtes
        choices=[
            ('S', 'Surveillant'),
            ('RS', 'Responsable + Surveillant'),
            ('R', 'Responsable Seulement'),
        ],
        verbose_name="Rôle"
    )

    class Meta:
        verbose_name = "Affectation"
        verbose_name_plural = "Affectations"
        unique_together = ('session', 'enseignant')  # Un enseignant ne peut pas être affecté deux fois à la même session

    def __str__(self):
        return f"{self.enseignant} - {self.session} ({self.role})"

: mon but est d'affecter les profs aux sessions des examens d'une maniere que pour chaque prof je dois essayer le maximum de doner  des seance de surveillance successifs pour un meme jour et des jours de surveillance aussi successifs : ceci est une pseudo code incomplet pour la logique d'affectations :
- créer une liste de jours contenants pour chaque jourla liste des sessions qui vont etre passé ce jour là.
pour jour:jours 
//affecter tout d'abord les profs aux sessions dont ils sont responsable ce jour là
pour session: jour.sessions
R_prof= chercher le prof responsable de la session dans la liste des enseignant
Si  
R_prof.session _surveillance = 0

Créer nouveau affectations (session.id, R-prof.id, 'R')
 Sinon :

Créer nouveau affectations (session.id, R-prof.id, 'RS')

R-prof. total_Rs += 1  
R-prof. calculer_total ( )  
sessio.nb_prof_aff += 1 //incrementation du nombre de prof affecte à une session  
fin si 
fin pour 
//essayer de completer le nombre de profs qu'on a besoin pour surveiller  chaque session de ce jour par les profs qui ont été affectés pour surveiller des seances ce jour là(bien sur un prof e doit pas etre surveillant dans la meme seance du meme jour )  
pour sessio:jour.sessions

Si  
Session.nb_prof_aff < session.nb_salle*2

// affecter des prfs ayant déjà des affectations  
de jour là ( avec le role 'S' et faire les mise à jour nécessaire) et pour chaqur prof total ne dois pas depasser seance_surveillance    
fin si 
fin pour 
fin pour : donner moi le code django necessaire pour faire ce que je veux et comment je peux tester avec postman le resultat