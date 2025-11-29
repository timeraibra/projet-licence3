from django.apps import AppConfig


class EvenementsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'evenements'
    verbose_name = 'Gestion des événements'
    
    def ready(self):
        """
        Méthode appelée au démarrage de l'application.
        Utilisée pour enregistrer les signaux si nécessaire.
        """
        pass