# Create your models here.
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone

class Utilisateur(AbstractUser):
    """Modèle utilisateur personnalisé"""
    ROLE_CHOICES = [
        ('etudiant', 'Étudiant'),
        ('admin', 'Administrateur'),
    ]
    
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='etudiant')
    departement = models.CharField(max_length=100, blank=True)
    telephone = models.CharField(max_length=20, blank=True)
    
    class Meta:
        verbose_name = 'Utilisateur'
        verbose_name_plural = 'Utilisateurs'
    
    def __str__(self):
        return f"{self.get_full_name()} ({self.role})"
    
    def est_admin(self):
        return self.role == 'admin'


class Evenement(models.Model):
    """Modèle pour les événements universitaires"""
    CATEGORIE_CHOICES = [
        ('conference', 'Conférence'),
        ('soutenance', 'Soutenance'),
        ('atelier', 'Atelier'),
        ('culturel', 'Activité Culturelle'),
        ('autre', 'Autre'),
    ]
    
    STATUT_CHOICES = [
        ('en_attente', 'En attente de validation'),
        ('valide', 'Validé'),
        ('refuse', 'Refusé'),
        ('annule', 'Annulé'),
    ]
    
    titre = models.CharField(max_length=200)
    description = models.TextField()
    date_debut = models.DateTimeField()
    date_fin = models.DateTimeField()
    lieu = models.CharField(max_length=200)
    categorie = models.CharField(max_length=20, choices=CATEGORIE_CHOICES)
    capacite_max = models.IntegerField(default=50, help_text="Nombre maximum de participants")
    
    organisateur = models.ForeignKey(Utilisateur, on_delete=models.CASCADE, related_name='evenements_organises')
    statut = models.CharField(max_length=20, choices=STATUT_CHOICES, default='en_attente')
    
    date_creation = models.DateTimeField(auto_now_add=True)
    date_modification = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Événement'
        verbose_name_plural = 'Événements'
        ordering = ['date_debut']
    
    def __str__(self):
        return f"{self.titre} - {self.date_debut.strftime('%d/%m/%Y')}"
    
    def est_complet(self):
        """Vérifie si l'événement a atteint sa capacité maximale"""
        return self.inscriptions.filter(statut='confirmee').count() >= self.capacite_max
    
    def nombre_inscrits(self):
        """Retourne le nombre d'inscrits confirmés"""
        return self.inscriptions.filter(statut='confirmee').count()
    
    def est_passe(self):
        """Vérifie si l'événement est passé"""
        return self.date_fin < timezone.now()
    
    def peut_modifier(self, utilisateur):
        """Vérifie si l'utilisateur peut modifier cet événement"""
        return self.organisateur == utilisateur or utilisateur.est_admin()


class Inscription(models.Model):
    """Modèle pour les inscriptions aux événements"""
    STATUT_CHOICES = [
        ('en_attente', 'En attente'),
        ('confirmee', 'Confirmée'),
        ('annulee', 'Annulée'),
    ]
    
    evenement = models.ForeignKey(Evenement, on_delete=models.CASCADE, related_name='inscriptions')
    participant = models.ForeignKey(Utilisateur, on_delete=models.CASCADE, related_name='inscriptions')
    statut = models.CharField(max_length=20, choices=STATUT_CHOICES, default='confirmee')
    date_inscription = models.DateTimeField(auto_now_add=True)
    commentaire = models.TextField(blank=True)
    
    class Meta:
        verbose_name = 'Inscription'
        verbose_name_plural = 'Inscriptions'
        unique_together = ['evenement', 'participant']
        ordering = ['-date_inscription']
    
    def __str__(self):
        return f"{self.participant.get_full_name()} - {self.evenement.titre}"