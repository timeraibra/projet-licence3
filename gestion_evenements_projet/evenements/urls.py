from django.urls import path
from . import views  # ← CETTE LIGNE EST ESSENTIELLE

urlpatterns = [
    # Pages publiques
    path('', views.accueil, name='accueil'),
    path('inscription/', views.inscription_utilisateur, name='inscription'),
    path('connexion/', views.connexion, name='connexion'),
    path('deconnexion/', views.deconnexion, name='deconnexion'),
    
    # Tableau de bord
    path('tableau-bord/', views.tableau_bord, name='tableau_bord'),
    path('profil/', views.profil, name='profil'),
    path('gestion-utilisateurs/', views.gestion_utilisateurs, name='gestion_utilisateurs'),
    
    # Événements
    path('evenements/', views.liste_evenements, name='liste_evenements'),
    path('evenements/<int:pk>/', views.detail_evenement, name='detail_evenement'),
    path('evenements/creer/', views.creer_evenement, name='creer_evenement'),
    path('evenements/<int:pk>/modifier/', views.modifier_evenement, name='modifier_evenement'),
    path('evenements/<int:pk>/supprimer/', views.supprimer_evenement, name='supprimer_evenement'),
    path('evenements/<int:pk>/valider/', views.valider_evenement, name='valider_evenement'),
    
    # Inscriptions
    path('evenements/<int:pk>/inscrire/', views.inscrire_evenement, name='inscrire_evenement'),
    path('evenements/<int:pk>/annuler-inscription/', views.annuler_inscription, name='annuler_inscription'),
    
]