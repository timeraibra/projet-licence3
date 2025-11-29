# Create your tests here.
from django.test import TestCase, Client
from django.urls import reverse
from django.utils import timezone
from datetime import timedelta
from .models import Utilisateur, Evenement, Inscription


class UtilisateurModelTest(TestCase):
    """Tests pour le modèle Utilisateur"""
    
    def setUp(self):
        self.etudiant = Utilisateur.objects.create_user(
            username='etudiant_test',
            password='test123',
            first_name='Jean',
            last_name='Test',
            email='jean@test.com',
            role='etudiant'
        )
        
        self.admin = Utilisateur.objects.create_user(
            username='admin_test',
            password='test123',
            first_name='Admin',
            last_name='Test',
            email='admin@test.com',
            role='admin'
        )
    
    def test_utilisateur_creation(self):
        """Test de création d'un utilisateur"""
        self.assertEqual(self.etudiant.username, 'etudiant_test')
        self.assertEqual(self.etudiant.role, 'etudiant')
        self.assertFalse(self.etudiant.est_admin())
    
    def test_admin_role(self):
        """Test du rôle admin"""
        self.assertTrue(self.admin.est_admin())


class EvenementModelTest(TestCase):
    """Tests pour le modèle Evenement"""
    
    def setUp(self):
        self.organisateur = Utilisateur.objects.create_user(
            username='organisateur',
            password='test123',
            role='etudiant'
        )
        
        self.evenement = Evenement.objects.create(
            titre='Test Conférence',
            description='Description test',
            date_debut=timezone.now() + timedelta(days=7),
            date_fin=timezone.now() + timedelta(days=7, hours=2),
            lieu='Amphi A',
            categorie='conference',
            capacite_max=50,
            organisateur=self.organisateur,
            statut='valide'
        )
    
    def test_evenement_creation(self):
        """Test de création d'un événement"""
        self.assertEqual(self.evenement.titre, 'Test Conférence')
        self.assertEqual(self.evenement.statut, 'valide')
        self.assertEqual(self.evenement.nombre_inscrits(), 0)
    
    def test_evenement_complet(self):
        """Test si un événement est complet"""
        self.assertFalse(self.evenement.est_complet())
        
        # Créer des inscriptions jusqu'à la capacité max
        for i in range(50):
            participant = Utilisateur.objects.create_user(
                username=f'participant{i}',
                password='test123',
                role='etudiant'
            )
            Inscription.objects.create(
                evenement=self.evenement,
                participant=participant,
                statut='confirmee'
            )
        
        self.assertTrue(self.evenement.est_complet())
    
    def test_peut_modifier(self):
        """Test des permissions de modification"""
        self.assertTrue(self.evenement.peut_modifier(self.organisateur))
        
        autre_user = Utilisateur.objects.create_user(
            username='autre',
            password='test123',
            role='etudiant'
        )
        self.assertFalse(self.evenement.peut_modifier(autre_user))


class InscriptionModelTest(TestCase):
    """Tests pour le modèle Inscription"""
    
    def setUp(self):
        self.organisateur = Utilisateur.objects.create_user(
            username='organisateur',
            password='test123'
        )
        
        self.participant = Utilisateur.objects.create_user(
            username='participant',
            password='test123'
        )
        
        self.evenement = Evenement.objects.create(
            titre='Test Event',
            description='Test',
            date_debut=timezone.now() + timedelta(days=7),
            date_fin=timezone.now() + timedelta(days=7, hours=2),
            lieu='Test',
            categorie='conference',
            capacite_max=50,
            organisateur=self.organisateur,
            statut='valide'
        )
    
    def test_inscription_creation(self):
        """Test de création d'une inscription"""
        inscription = Inscription.objects.create(
            evenement=self.evenement,
            participant=self.participant,
            statut='confirmee'
        )
        
        self.assertEqual(inscription.statut, 'confirmee')
        self.assertEqual(self.evenement.nombre_inscrits(), 1)


class ViewsTest(TestCase):
    """Tests pour les vues"""
    
    def setUp(self):
        self.client = Client()
        self.user = Utilisateur.objects.create_user(
            username='testuser',
            password='test123',
            first_name='Test',
            last_name='User',
            email='test@test.com',
            role='etudiant'
        )
    
    def test_accueil_view(self):
        """Test de la page d'accueil"""
        response = self.client.get(reverse('accueil'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'evenements/accueil.html')
    
    def test_connexion_view(self):
        """Test de la page de connexion"""
        response = self.client.get(reverse('connexion'))
        self.assertEqual(response.status_code, 200)
    
    def test_tableau_bord_requires_login(self):
        """Test que le tableau de bord nécessite une connexion"""
        response = self.client.get(reverse('tableau_bord'))
        self.assertEqual(response.status_code, 302)  # Redirection
    
    def test_tableau_bord_with_login(self):
        """Test du tableau de bord avec connexion"""
        self.client.login(username='testuser', password='test123')
        response = self.client.get(reverse('tableau_bord'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'evenements/tableau_bord.html')
    
    def test_creer_evenement_requires_login(self):
        """Test que la création d'événement nécessite une connexion"""
        response = self.client.get(reverse('creer_evenement'))
        self.assertEqual(response.status_code, 302)


class IntegrationTest(TestCase):
    """Tests d'intégration"""
    
    def setUp(self):
        self.client = Client()
    
    def test_workflow_complet(self):
        """Test du workflow complet : inscription, connexion, création événement"""
        # 1. Inscription
        response = self.client.post(reverse('inscription'), {
            'username': 'newuser',
            'password1': 'ComplexPass123!',
            'password2': 'ComplexPass123!',
            'first_name': 'New',
            'last_name': 'User',
            'email': 'new@test.com',
            'role': 'etudiant'
        })
        
        # 2. Vérifier que l'utilisateur est créé
        user_exists = Utilisateur.objects.filter(username='newuser').exists()
        self.assertTrue(user_exists)
        
        # 3. Créer un événement
        self.client.login(username='newuser', password='ComplexPass123!')
        response = self.client.post(reverse('creer_evenement'), {
            'titre': 'Nouvel événement',
            'description': 'Description de test',
            'date_debut': (timezone.now() + timedelta(days=7)).strftime('%Y-%m-%dT%H:%M'),
            'date_fin': (timezone.now() + timedelta(days=7, hours=2)).strftime('%Y-%m-%dT%H:%M'),
            'lieu': 'Salle test',
            'categorie': 'conference',
            'capacite_max': 50
        })
        
        # 4. Vérifier que l'événement est créé
        event_exists = Evenement.objects.filter(titre='Nouvel événement').exists()
        self.assertTrue(event_exists)