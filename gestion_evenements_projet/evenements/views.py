from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q, Count
from django.utils import timezone
from .models import Utilisateur, Evenement, Inscription
from .forms import InscriptionForm, ConnexionForm, EvenementForm, UtilisateurForm, ProfilForm
from .emails import (
    envoyer_email_inscription, 
    envoyer_email_annulation, 
    envoyer_email_validation_evenement
)


def accueil(request):
    """Page d'accueil avec liste des événements validés"""
    evenements_a_venir = Evenement.objects.filter(
        statut='valide',
        date_debut__gte=timezone.now()
    ).order_by('date_debut')[:6]
    
    context = {
        'evenements': evenements_a_venir,
    }
    return render(request, 'evenements/accueil.html', context)


def inscription_utilisateur(request):
    """Inscription d'un nouvel utilisateur"""
    if request.user.is_authenticated:
        return redirect('tableau_bord')
    
    if request.method == 'POST':
        form = UtilisateurForm(request.POST)
        if form.is_valid():
            utilisateur = form.save()
            login(request, utilisateur)
            messages.success(request, 'Inscription réussie ! Bienvenue sur la plateforme.')
            return redirect('tableau_bord')
    else:
        form = UtilisateurForm()
    
    return render(request, 'evenements/inscription.html', {'form': form})


def connexion(request):
    """Connexion d'un utilisateur"""
    if request.user.is_authenticated:
        return redirect('tableau_bord')
    
    if request.method == 'POST':
        form = ConnexionForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                messages.success(request, f'Bienvenue {user.get_full_name()} !')
                return redirect('tableau_bord')
            else:
                messages.error(request, 'Identifiants incorrects.')
    else:
        form = ConnexionForm()
    
    return render(request, 'evenements/connexion.html', {'form': form})


@login_required
def deconnexion(request):
    """Déconnexion de l'utilisateur"""
    logout(request)
    messages.info(request, 'Vous avez été déconnecté.')
    return redirect('accueil')


@login_required
def tableau_bord(request):
    """Tableau de bord personnalisé selon le rôle"""
    utilisateur = request.user
    
    # Événements organisés par l'utilisateur
    mes_evenements = Evenement.objects.filter(organisateur=utilisateur)
    
    # Inscriptions de l'utilisateur
    mes_inscriptions = Inscription.objects.filter(
        participant=utilisateur,
        statut='confirmee'
    ).select_related('evenement')
    
    # Événements en attente de validation (pour admin)
    evenements_en_attente = None
    if utilisateur.est_admin():
        evenements_en_attente = Evenement.objects.filter(statut='en_attente')
    
    # Statistiques
    stats = {
        'nb_evenements_organises': mes_evenements.count(),
        'nb_inscriptions': mes_inscriptions.count(),
        'nb_participants_total': sum([e.nombre_inscrits() for e in mes_evenements]),
    }
    
    context = {
        'mes_evenements': mes_evenements,
        'mes_inscriptions': mes_inscriptions,
        'evenements_en_attente': evenements_en_attente,
        'stats': stats,
        'now': timezone.now(),  # Ajout de la date actuelle
    }
    return render(request, 'evenements/tableau_bord.html', context)


@login_required
def liste_evenements(request):
    """Liste de tous les événements avec filtres"""
    evenements = Evenement.objects.filter(statut='valide')
    
    # Filtres
    categorie = request.GET.get('categorie')
    recherche = request.GET.get('recherche')
    
    if categorie:
        evenements = evenements.filter(categorie=categorie)
    
    if recherche:
        evenements = evenements.filter(
            Q(titre__icontains=recherche) |
            Q(description__icontains=recherche) |
            Q(lieu__icontains=recherche)
        )
    
    # Séparer les événements à venir et passés
    maintenant = timezone.now()
    evenements_a_venir = evenements.filter(date_debut__gte=maintenant).order_by('date_debut')
    evenements_passes = evenements.filter(date_debut__lt=maintenant).order_by('-date_debut')
    
    context = {
        'evenements_a_venir': evenements_a_venir,
        'evenements_passes': evenements_passes,
        'categories': Evenement.CATEGORIE_CHOICES,
        'categorie_selectionnee': categorie,
        'recherche': recherche,
    }
    return render(request, 'evenements/liste_evenements.html', context)


@login_required
def detail_evenement(request, pk):
    """Détail d'un événement"""
    evenement = get_object_or_404(Evenement, pk=pk)
    
    # Vérifier si l'utilisateur est déjà inscrit
    est_inscrit = Inscription.objects.filter(
        evenement=evenement,
        participant=request.user,
        statut='confirmee'
    ).exists()
    
    # Liste des inscrits (visible par l'organisateur et admin)
    inscrits = None
    if evenement.peut_modifier(request.user):
        inscrits = evenement.inscriptions.filter(statut='confirmee').select_related('participant')
    
    context = {
        'evenement': evenement,
        'est_inscrit': est_inscrit,
        'inscrits': inscrits,
    }
    return render(request, 'evenements/detail_evenement.html', context)


@login_required
def creer_evenement(request):
    """Créer un nouvel événement"""
    if request.method == 'POST':
        form = EvenementForm(request.POST)
        if form.is_valid():
            evenement = form.save(commit=False)
            evenement.organisateur = request.user
            evenement.save()
            messages.success(request, 'Événement créé avec succès ! Il sera visible après validation.')
            return redirect('detail_evenement', pk=evenement.pk)
    else:
        form = EvenementForm()
    
    return render(request, 'evenements/creer_evenement.html', {'form': form})


@login_required
def modifier_evenement(request, pk):
    """Modifier un événement existant"""
    evenement = get_object_or_404(Evenement, pk=pk)
    
    if not evenement.peut_modifier(request.user):
        messages.error(request, "Vous n'avez pas la permission de modifier cet événement.")
        return redirect('detail_evenement', pk=pk)
    
    if request.method == 'POST':
        form = EvenementForm(request.POST, instance=evenement)
        if form.is_valid():
            form.save()
            messages.success(request, 'Événement modifié avec succès !')
            return redirect('detail_evenement', pk=pk)
    else:
        form = EvenementForm(instance=evenement)
    
    return render(request, 'evenements/modifier_evenement.html', {'form': form, 'evenement': evenement})


@login_required
def supprimer_evenement(request, pk):
    """Supprimer un événement"""
    evenement = get_object_or_404(Evenement, pk=pk)
    
    if not evenement.peut_modifier(request.user):
        messages.error(request, "Vous n'avez pas la permission de supprimer cet événement.")
        return redirect('detail_evenement', pk=pk)
    
    if request.method == 'POST':
        evenement.delete()
        messages.success(request, 'Événement supprimé avec succès.')
        return redirect('tableau_bord')
    
    return render(request, 'evenements/supprimer_evenement.html', {'evenement': evenement})


@login_required
def valider_evenement(request, pk):
    """Valider ou refuser un événement (admin uniquement)"""
    if not request.user.est_admin():
        messages.error(request, "Vous n'avez pas la permission d'effectuer cette action.")
        return redirect('tableau_bord')
    
    evenement = get_object_or_404(Evenement, pk=pk)
    action = request.POST.get('action')
    
    if action == 'valider':
        evenement.statut = 'valide'
        evenement.save()
        # Envoyer email à l'organisateur
        envoyer_email_validation_evenement(evenement)
        messages.success(request, f'Événement "{evenement.titre}" validé avec succès.')
    elif action == 'refuser':
        evenement.statut = 'refuse'
        evenement.save()
        messages.warning(request, f'Événement "{evenement.titre}" refusé.')
    
    return redirect('tableau_bord')


@login_required
def inscrire_evenement(request, pk):
    """S'inscrire à un événement"""
    evenement = get_object_or_404(Evenement, pk=pk)
    
    # Vérifications
    if evenement.statut != 'valide':
        messages.error(request, "Cet événement n'est pas encore validé.")
        return redirect('detail_evenement', pk=pk)
    
    if evenement.est_complet():
        messages.error(request, "Cet événement est complet.")
        return redirect('detail_evenement', pk=pk)
    
    if evenement.est_passe():
        messages.error(request, "Cet événement est déjà passé.")
        return redirect('detail_evenement', pk=pk)
    
    # Créer ou récupérer l'inscription
    inscription, created = Inscription.objects.get_or_create(
        evenement=evenement,
        participant=request.user,
        defaults={'statut': 'confirmee'}
    )
    
    if created:
        # Envoyer email de confirmation
        envoyer_email_inscription(inscription)
        messages.success(request, 'Inscription confirmée ! Un email de confirmation vous a été envoyé.')
    else:
        if inscription.statut == 'annulee':
            inscription.statut = 'confirmee'
            inscription.save()
            envoyer_email_inscription(inscription)
            messages.success(request, 'Inscription réactivée ! Un email de confirmation vous a été envoyé.')
        else:
            messages.info(request, 'Vous êtes déjà inscrit à cet événement.')
    
    return redirect('detail_evenement', pk=pk)


@login_required
def annuler_inscription(request, pk):
    """Annuler son inscription à un événement"""
    evenement = get_object_or_404(Evenement, pk=pk)
    
    try:
        inscription = Inscription.objects.get(
            evenement=evenement,
            participant=request.user,
            statut='confirmee'
        )
        inscription.statut = 'annulee'
        inscription.save()
        # Envoyer email d'annulation
        envoyer_email_annulation(inscription)
        messages.success(request, 'Inscription annulée. Un email de confirmation vous a été envoyé.')
    except Inscription.DoesNotExist:
        messages.error(request, "Vous n'êtes pas inscrit à cet événement.")
    
    return redirect('detail_evenement', pk=pk)


@login_required
def profil(request):
    """Afficher et modifier le profil utilisateur"""
    if request.method == 'POST':
        # Utiliser ProfilForm au lieu de UtilisateurForm
        form = ProfilForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profil mis à jour avec succès.')
            return redirect('profil')
    else:
        form = ProfilForm(instance=request.user)
    
    return render(request, 'evenements/profil.html', {'form': form})


@login_required
def gestion_utilisateurs(request):
    """
    Liste de tous les utilisateurs inscrits (accessible uniquement aux admins)
    """
    if not request.user.est_admin():
        messages.error(request, "Vous n'avez pas accès à cette page.")
        return redirect('tableau_bord')
    
    # Récupérer tous les utilisateurs
    utilisateurs = Utilisateur.objects.all().order_by('-date_joined')
    
    # Filtres
    role_filtre = request.GET.get('role')
    recherche = request.GET.get('recherche')
    departement_filtre = request.GET.get('departement')
    
    if role_filtre:
        utilisateurs = utilisateurs.filter(role=role_filtre)
    
    if recherche:
        utilisateurs = utilisateurs.filter(
            Q(username__icontains=recherche) |
            Q(first_name__icontains=recherche) |
            Q(last_name__icontains=recherche) |
            Q(email__icontains=recherche)
        )
    
    if departement_filtre:
        utilisateurs = utilisateurs.filter(departement__icontains=departement_filtre)
    
    # Statistiques
    stats = {
        'total_utilisateurs': Utilisateur.objects.count(),
        'total_etudiants': Utilisateur.objects.filter(role='etudiant').count(),
        'total_admins': Utilisateur.objects.filter(role='admin').count(),
        'nouveaux_7_jours': Utilisateur.objects.filter(
            date_joined__gte=timezone.now() - timezone.timedelta(days=7)
        ).count(),
    }
    
    # Départements uniques pour le filtre
    departements = Utilisateur.objects.exclude(
        departement=''
    ).values_list('departement', flat=True).distinct()
    
    context = {
        'utilisateurs': utilisateurs,
        'stats': stats,
        'departements': departements,
        'role_filtre': role_filtre,
        'recherche': recherche,
        'departement_filtre': departement_filtre,
    }
    
    return render(request, 'evenements/gestion_utilisateurs.html', context)