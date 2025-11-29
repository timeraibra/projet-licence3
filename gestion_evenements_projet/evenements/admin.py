# Register your models here.
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Utilisateur, Evenement, Inscription


@admin.register(Utilisateur)
class UtilisateurAdmin(UserAdmin):
    """Configuration de l'admin pour le modèle Utilisateur"""
    list_display = ['username', 'email', 'first_name', 'last_name', 'role', 'departement']
    list_filter = ['role', 'departement', 'is_staff', 'is_active']
    search_fields = ['username', 'first_name', 'last_name', 'email']
    
    fieldsets = UserAdmin.fieldsets + (
        ('Informations supplémentaires', {
            'fields': ('role', 'departement', 'telephone')
        }),
    )
    
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Informations supplémentaires', {
            'fields': ('role', 'departement', 'telephone', 'first_name', 'last_name', 'email')
        }),
    )


@admin.register(Evenement)
class EvenementAdmin(admin.ModelAdmin):
    """Configuration de l'admin pour le modèle Evenement"""
    list_display = ['titre', 'categorie', 'date_debut', 'lieu', 'organisateur', 'statut', 'nombre_inscrits', 'capacite_max']
    list_filter = ['statut', 'categorie', 'date_debut']
    search_fields = ['titre', 'description', 'lieu', 'organisateur__username']
    date_hierarchy = 'date_debut'
    ordering = ['-date_debut']
    
    fieldsets = (
        ('Informations générales', {
            'fields': ('titre', 'description', 'categorie')
        }),
        ('Date et lieu', {
            'fields': ('date_debut', 'date_fin', 'lieu')
        }),
        ('Organisation', {
            'fields': ('organisateur', 'capacite_max', 'statut')
        }),
    )
    
    readonly_fields = ['date_creation', 'date_modification']
    
    def save_model(self, request, obj, form, change):
        if not change:  # Si c'est une nouvelle création
            obj.organisateur = request.user
        super().save_model(request, obj, form, change)
    
    actions = ['valider_evenements', 'refuser_evenements']
    
    def valider_evenements(self, request, queryset):
        count = queryset.update(statut='valide')
        self.message_user(request, f'{count} événement(s) validé(s).')
    valider_evenements.short_description = "Valider les événements sélectionnés"
    
    def refuser_evenements(self, request, queryset):
        count = queryset.update(statut='refuse')
        self.message_user(request, f'{count} événement(s) refusé(s).')
    refuser_evenements.short_description = "Refuser les événements sélectionnés"


@admin.register(Inscription)
class InscriptionAdmin(admin.ModelAdmin):
    """Configuration de l'admin pour le modèle Inscription"""
    list_display = ['participant', 'evenement', 'statut', 'date_inscription']
    list_filter = ['statut', 'date_inscription', 'evenement__categorie']
    search_fields = ['participant__username', 'participant__email', 'evenement__titre']
    date_hierarchy = 'date_inscription'
    
    fieldsets = (
        ('Inscription', {
            'fields': ('evenement', 'participant', 'statut')
        }),
        ('Détails', {
            'fields': ('commentaire', 'date_inscription')
        }),
    )
    
    readonly_fields = ['date_inscription']