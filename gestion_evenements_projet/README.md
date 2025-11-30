# Plateforme de Gestion d'Événements Universitaires

## 📋 Description

Application web Django permettant aux étudiants et enseignants d'organiser et de gérer des événements universitaires (conférences, soutenances, activités culturelles, etc.).

## ✨ Fonctionnalités

### Gestion des utilisateurs
- ✅ Inscription et authentification (étudiant / administrateur)
- ✅ Gestion des rôles et permissions
- ✅ Profil utilisateur personnalisé (nom, email, département, téléphone)

### Gestion des événements
- ✅ Création d'événements (titre, description, date, lieu, organisateur, capacité)
- ✅ Modification et suppression par l'organisateur
- ✅ Validation des événements par un administrateur
- ✅ Catégorisation (conférence, soutenance, atelier, culturel)
- ✅ Gestion des statuts (en attente, validé, refusé, annulé)

### Gestion des inscriptions
- ✅ Inscription aux événements pour les étudiants
- ✅ Liste des inscrits visible par l'organisateur
- ✅ Confirmation et annulation d'inscription
- ✅ Limitation de capacité

### Tableau de bord
- ✅ Affichage des événements par date
- ✅ Filtrage par catégorie et recherche
- ✅ Statistiques (événements organisés, participants, inscriptions)
- ✅ Vue personnalisée selon le rôle

## 🛠️ Technologies utilisées

- **Backend** : Python 3.x, Django 5.0
- **Base de données** : SQLite (par défaut) / PostgreSQL (optionnel)
- **Frontend** : Templates Django, HTML5, CSS3, Bootstrap 5.3
- **Authentification** : Système natif Django

## 📦 Installation

### Prérequis
- Python 3.8 ou supérieur
- pip (gestionnaire de paquets Python)
- virtualenv (recommandé)

### Étapes d'installation

1. **Cloner le projet**
```bash
git clone <url-du-repo>
cd gestion_evenements
```

2. **Créer un environnement virtuel**
```bash
python -m venv venv
source venv/bin/activate  # Sur Windows: venv\Scripts\activate
```

3. **Installer les dépendances**
```bash
pip install django
# Pour PostgreSQL (optionnel):
# pip install psycopg2-binary
```

4. **Configuration de la base de données**

Éditez `gestion_evenements/settings.py` si vous voulez utiliser PostgreSQL :
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'gestion_evenements',
        'USER': 'votre_utilisateur',
        'PASSWORD': 'votre_mot_de_passe',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

5. **Appliquer les migrations**
```bash
python manage.py makemigrations
python manage.py migrate
```

6. **Créer un superutilisateur (administrateur)**
```bash
python manage.py createsuperuser
```

7. **Collecter les fichiers statiques**
```bash
python manage.py collectstatic
```

8. **Lancer le serveur de développement**
```bash
python manage.py runserver
```

9. **Accéder à l'application**
- Application : http://localhost:8000/
- Interface admin : http://localhost:8000/admin/

## 📁 Structure du projet

```
gestion_evenements/
├── gestion_evenements/          # Configuration du projet
│   ├── __init__.py
│   ├── settings.py              # Configuration Django
│   ├── urls.py                  # URLs principales
│   └── wsgi.py
├── evenements/                  # Application principale
│   ├── migrations/              # Migrations de base de données
│   ├── templates/               # Templates HTML
│   │   └── evenements/
│   │       ├── base.html
│   │       ├── accueil.html
│   │       ├── tableau_bord.html
│   │       ├── liste_evenements.html
│   │       ├── detail_evenement.html
│   │       ├── creer_evenement.html
│   │       ├── modifier_evenement.html
│   │       ├── supprimer_evenement.html
│   │       ├── inscription.html
│   │       ├── connexion.html
│   │       └── profil.html
│   ├── __init__.py
│   ├── admin.py                 # Configuration admin
│   ├── models.py                # Modèles de données
│   ├── views.py                 # Vues
│   ├── forms.py                 # Formulaires
│   └── urls.py                  # URLs de l'app
├── manage.py
└── README.md
```

## 👥 Utilisation

### Rôles et permissions

**Étudiant :**
- Consulter les événements validés
- S'inscrire/se désinscrire des événements
- Créer des événements (soumis à validation)
- Gérer ses propres événements

**Administrateur :**
- Toutes les permissions d'un étudiant
- Valider/refuser les événements
- Modifier/supprimer tous les événements
- Accès à l'interface d'administration Django

### Workflow typique

1. **Inscription d'un utilisateur**
   - Accéder à la page d'inscription
   - Remplir le formulaire (rôle par défaut : étudiant)
   - Connexion automatique après inscription

2. **Création d'un événement**
   - Se connecter
   - Cliquer sur "Créer un événement"
   - Remplir les détails de l'événement
   - Attendre la validation par un admin

3. **Validation (Admin)**
   - Accéder au tableau de bord
   - Section "Événements en attente"
   - Valider ou refuser les événements

4. **Inscription à un événement**
   - Parcourir la liste des événements
   - Cliquer sur un événement
   - Cliquer sur "S'inscrire"

## 🔒 Sécurité

- Authentification requise pour les actions sensibles
- CSRF protection activée
- Validation des formulaires côté serveur
- Permissions basées sur les rôles
- Mots de passe hashés (système Django)

## 🚀 Déploiement en production

### Checklist de sécurité

1. Modifier `SECRET_KEY` dans settings.py
2. Définir `DEBUG = False`
3. Configurer `ALLOWED_HOSTS`
4. Utiliser PostgreSQL au lieu de SQLite
5. Configurer les fichiers statiques avec un serveur web
6. Utiliser HTTPS
7. Configurer les variables d'environnement

### Exemple avec Gunicorn

```bash
pip install gunicorn
gunicorn gestion_evenements.wsgi:application
```

## 📝 Données de test

Pour créer des données de test :

```bash
python manage.py shell
```

```python
from evenements.models import Utilisateur, Evenement
from django.utils import timezone
from datetime import timedelta

# Créer un étudiant
etudiant = Utilisateur.objects.create_user(
    username='etudiant1',
    password='test1234',
    first_name='Jean',
    last_name='Dupont',
    email='jean@exemple.com',
    role='etudiant',
    departement='Informatique'
)

# Créer un événement
evenement = Evenement.objects.create(
    titre='Conférence IA',
    description='Découvrez les dernières avancées en intelligence artificielle',
    date_debut=timezone.now() + timedelta(days=7),
    date_fin=timezone.now() + timedelta(days=7, hours=2),
    lieu='Amphi A',
    categorie='conference',
    capacite_max=100,
    organisateur=etudiant,
    statut='valide'
)
```

## 🤝 Contribution

Les contributions sont les bienvenues ! Pour contribuer :

1. Fork le projet
2. Créer une branche (`git checkout -b feature/amelioration`)
3. Commit les changements (`git commit -m 'Ajout fonctionnalité'`)
4. Push vers la branche (`git push origin feature/amelioration`)
5. Ouvrir une Pull Request

## 📄 Licence

Ce projet est développé dans un cadre pédagogique.

## 📧 Contact

Pour toute question ou suggestion, veuillez contacter l'équipe de développement.

## 🐛 Problèmes connus

- Les notifications par email ne sont pas implémentées
- L'export des listes de participants n'est pas disponible
- Pas de système de commentaires sur les événements

## 🔮 Améliorations futures

- [ ] Notifications par email
- [ ] Export PDF/Excel des listes
- [ ] Système de commentaires
- [ ] Calendrier interactif
- [ ] API REST
- [ ] Application mobile
- [ ] Système de tags pour les événements
- [ ] Gestion des pièces jointes