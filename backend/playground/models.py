
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
        constraints = [
            models.UniqueConstraint(
                fields=['nom_prenom', 'departement', 'grade'],
                name='unique_enseignant'
            )
        ]

    def __str__(self):
        return f"{self.nom_prenom} - {self.departement}"

    @property
    def volume_horaire_total(self):
        return self.heures_td + self.heures_tp

    def calculer_total(self):
        """Méthode pour calculer et mettre à jour le champ 'total'."""
        self.total = self.total_S + self.total_RS 

    @classmethod       
    def enseignants_total_inferieur_surveillance(cls):
        """
        Retourne une liste d'enseignants dont le total est inférieur au nombre de séances de surveillance.
        """
        return cls.objects.filter(total__lt=models.F('seances_surveillance'))
    @staticmethod
    def rechercher_par_nom(nom):
        """
        Retourne une liste d'enseignants dont le nom contient la chaîne de recherche.
        """
        return Enseignant.objects.filter(nom_prenom__icontains=nom)
class Session(models.Model):
    SEANCE_CHOICES = [
        ('s1', '08:30-10:00'),
        ('s2', '10:45-12:15'), 
        ('s3', '13:00-14:30'),
        ('s4', '15:15-16:45'),
    ]
    
    session_id = models.CharField(max_length=20)
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
    role = models.CharField(max_length=4)
    unique_together = ('session', 'enseignant')
    class Meta:
        verbose_name = "Affectation"
        verbose_name_plural = "Affectations"
        unique_together = ('session', 'enseignant')  # Un enseignant ne peut pas être affecté deux fois à la même session

    def __str__(self):
        return f"{self.enseignant} - {self.session} ({self.role})"


class Devoir(models.Model):
    matiere = models.CharField(max_length=50)
    profResponsable = models.CharField(max_length=200, verbose_name="Nom et Prénom")
    session = models.ForeignKey(
        'Session',  # Référence au modèle Session
        on_delete=models.CASCADE,  # Si la session est supprimée, les devoirs associés seront également supprimés
        related_name='devoirs'  # Nom utilisé pour accéder aux devoirs depuis une instance de Session
    )

    def __str__(self):
        return f"{self.profResponsable} - {self.matiere}"



class Disponibilite(models.Model):
    SEANCE_CHOICES = [
        ('s1', '08:30-10:00'),
        ('s2', '10:45-12:15'), 
        ('s3', '13:00-14:30'),
        ('s4', '15:15-16:45'),
    ]
    
    enseignant = models.ForeignKey(Enseignant, on_delete=models.CASCADE, related_name='disponibilites')
    indisponibilites = models.JSONField(
        default=list,
        help_text="Liste des indisponibilités sous forme [{'date': 'YYYY-MM-DD', 'seance': 's1'}, ...]"
    )

    class Meta:
        verbose_name = "Disponibilité"
        verbose_name_plural = "Disponibilités"
        ordering = ['enseignant']

    def __str__(self):
        return f"Disponibilités de {self.enseignant.nom_prenom}"
    


