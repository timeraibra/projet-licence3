from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Utilisateur, Evenement, Inscription


class UtilisateurForm(UserCreationForm):
    """Formulaire d'inscription/modification utilisateur"""
    first_name = forms.CharField(
        max_length=30,
        required=True,
        label='Prénom',
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    last_name = forms.CharField(
        max_length=30,
        required=True,
        label='Nom',
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    email = forms.EmailField(
        required=True,
        label='Email',
        widget=forms.EmailInput(attrs={'class': 'form-control'})
    )
    departement = forms.CharField(
        max_length=100,
        required=False,
        label='Département',
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    telephone = forms.CharField(
        max_length=20,
        required=False,
        label='Téléphone',
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    
    class Meta:
        model = Utilisateur
        fields = ['username', 'first_name', 'last_name', 'email', 'departement', 'telephone', 'role', 'password1', 'password2']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'role': forms.Select(attrs={'class': 'form-control'}),
        }
        labels = {
            'username': "Nom d'utilisateur",
            'role': 'Rôle',
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].widget.attrs.update({'class': 'form-control'})
        self.fields['password2'].widget.attrs.update({'class': 'form-control'})
        self.fields['password1'].label = 'Mot de passe'
        self.fields['password2'].label = 'Confirmer le mot de passe'


class ConnexionForm(forms.Form):
    """Formulaire de connexion"""
    username = forms.CharField(
        label="Nom d'utilisateur",
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    password = forms.CharField(
        label='Mot de passe',
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )


class EvenementForm(forms.ModelForm):
    """Formulaire de création/modification d'événement"""
    date_debut = forms.DateTimeField(
        label='Date et heure de début',
        widget=forms.DateTimeInput(attrs={
            'class': 'form-control',
            'type': 'datetime-local'
        }),
        input_formats=['%Y-%m-%dT%H:%M']
    )
    date_fin = forms.DateTimeField(
        label='Date et heure de fin',
        widget=forms.DateTimeInput(attrs={
            'class': 'form-control',
            'type': 'datetime-local'
        }),
        input_formats=['%Y-%m-%dT%H:%M']
    )
    
    class Meta:
        model = Evenement
        fields = ['titre', 'description', 'date_debut', 'date_fin', 'lieu', 'categorie', 'capacite_max']
        widgets = {
            'titre': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'lieu': forms.TextInput(attrs={'class': 'form-control'}),
            'categorie': forms.Select(attrs={'class': 'form-control'}),
            'capacite_max': forms.NumberInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'titre': 'Titre',
            'description': 'Description',
            'lieu': 'Lieu',
            'categorie': 'Catégorie',
            'capacite_max': 'Capacité maximale',
        }
    
    def clean(self):
        cleaned_data = super().clean()
        date_debut = cleaned_data.get('date_debut')
        date_fin = cleaned_data.get('date_fin')
        
        if date_debut and date_fin:
            if date_fin <= date_debut:
                raise forms.ValidationError(
                    "La date de fin doit être postérieure à la date de début."
                )
        
        return cleaned_data


class InscriptionForm(forms.ModelForm):
    """Formulaire d'inscription à un événement"""
    class Meta:
        model = Inscription
        fields = ['commentaire']
        widgets = {
            'commentaire': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Commentaire (optionnel)'
            }),
        }
        labels = {
            'commentaire': 'Commentaire',
        }