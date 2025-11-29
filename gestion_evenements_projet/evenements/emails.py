from django.core.mail import send_mail, send_mass_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings


def envoyer_email_inscription(inscription):
    """
    Envoie un email de confirmation d'inscription au participant
    """
    evenement = inscription.evenement
    participant = inscription.participant
    
    sujet = f"✅ Confirmation d'inscription - {evenement.titre}"
    
    # Template HTML de l'email
    contexte = {
        'participant': participant,
        'evenement': evenement,
        'inscription': inscription,
    }
    
    message_html = f"""
    <html>
        <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
            <div style="max-width: 600px; margin: 0 auto; padding: 20px; border: 1px solid #ddd; border-radius: 10px;">
                <h2 style="color: #667eea;">✅ Inscription confirmée !</h2>
                
                <p>Bonjour <strong>{participant.get_full_name()}</strong>,</p>
                
                <p>Votre inscription à l'événement suivant a bien été prise en compte :</p>
                
                <div style="background: #f9fafb; padding: 15px; border-radius: 8px; margin: 20px 0;">
                    <h3 style="margin-top: 0; color: #667eea;">{evenement.titre}</h3>
                    <p><strong>📅 Date :</strong> {evenement.date_debut.strftime('%d/%m/%Y à %H:%M')}</p>
                    <p><strong>📍 Lieu :</strong> {evenement.lieu}</p>
                    <p><strong>👤 Organisateur :</strong> {evenement.organisateur.get_full_name()}</p>
                </div>
                
                <p><strong>Description :</strong></p>
                <p>{evenement.description}</p>
                
                <div style="margin-top: 30px; padding: 15px; background: #e0f2fe; border-radius: 8px;">
                    <p style="margin: 0;"><strong>💡 Conseils :</strong></p>
                    <ul>
                        <li>Arrivez 10 minutes avant le début</li>
                        <li>N'oubliez pas votre pièce d'identité si nécessaire</li>
                        <li>En cas d'empêchement, annulez votre inscription depuis votre espace</li>
                    </ul>
                </div>
                
                <p style="margin-top: 30px;">À très bientôt !</p>
                <p style="color: #888; font-size: 12px;">
                    Cet email a été envoyé automatiquement, merci de ne pas y répondre.
                </p>
            </div>
        </body>
    </html>
    """
    
    message_texte = strip_tags(message_html)
    
    try:
        send_mail(
            sujet,
            message_texte,
            settings.DEFAULT_FROM_EMAIL,
            [participant.email],
            html_message=message_html,
            fail_silently=False,
        )
        return True
    except Exception as e:
        print(f"Erreur d'envoi d'email : {e}")
        return False


def envoyer_email_annulation(inscription):
    """
    Envoie un email de confirmation d'annulation
    """
    evenement = inscription.evenement
    participant = inscription.participant
    
    sujet = f"❌ Annulation d'inscription - {evenement.titre}"
    
    message_html = f"""
    <html>
        <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
            <div style="max-width: 600px; margin: 0 auto; padding: 20px; border: 1px solid #ddd; border-radius: 10px;">
                <h2 style="color: #ef4444;">❌ Inscription annulée</h2>
                
                <p>Bonjour <strong>{participant.get_full_name()}</strong>,</p>
                
                <p>Votre inscription à l'événement suivant a bien été annulée :</p>
                
                <div style="background: #fef2f2; padding: 15px; border-radius: 8px; margin: 20px 0;">
                    <h3 style="margin-top: 0;">{evenement.titre}</h3>
                    <p><strong>📅 Date :</strong> {evenement.date_debut.strftime('%d/%m/%Y à %H:%M')}</p>
                    <p><strong>📍 Lieu :</strong> {evenement.lieu}</p>
                </div>
                
                <p>Vous pouvez vous réinscrire à tout moment si vous changez d'avis (sous réserve de places disponibles).</p>
                
                <p style="margin-top: 30px;">À bientôt sur notre plateforme !</p>
            </div>
        </body>
    </html>
    """
    
    message_texte = strip_tags(message_html)
    
    try:
        send_mail(
            sujet,
            message_texte,
            settings.DEFAULT_FROM_EMAIL,
            [participant.email],
            html_message=message_html,
            fail_silently=False,
        )
        return True
    except Exception as e:
        print(f"Erreur d'envoi d'email : {e}")
        return False


def envoyer_email_validation_evenement(evenement):
    """
    Envoie un email à l'organisateur quand son événement est validé
    """
    organisateur = evenement.organisateur
    
    sujet = f"✅ Votre événement '{evenement.titre}' a été validé"
    
    message_html = f"""
    <html>
        <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
            <div style="max-width: 600px; margin: 0 auto; padding: 20px; border: 1px solid #ddd; border-radius: 10px;">
                <h2 style="color: #10b981;">✅ Événement validé !</h2>
                
                <p>Bonjour <strong>{organisateur.get_full_name()}</strong>,</p>
                
                <p>Bonne nouvelle ! Votre événement a été validé et est maintenant visible par tous les utilisateurs :</p>
                
                <div style="background: #f0fdf4; padding: 15px; border-radius: 8px; margin: 20px 0;">
                    <h3 style="margin-top: 0; color: #10b981;">{evenement.titre}</h3>
                    <p><strong>📅 Date :</strong> {evenement.date_debut.strftime('%d/%m/%Y à %H:%M')}</p>
                    <p><strong>📍 Lieu :</strong> {evenement.lieu}</p>
                    <p><strong>👥 Capacité :</strong> {evenement.capacite_max} places</p>
                </div>
                
                <p>Les étudiants peuvent maintenant s'inscrire à votre événement !</p>
                
                <p style="margin-top: 30px;">Bon succès pour votre événement !</p>
            </div>
        </body>
    </html>
    """
    
    message_texte = strip_tags(message_html)
    
    try:
        send_mail(
            sujet,
            message_texte,
            settings.DEFAULT_FROM_EMAIL,
            [organisateur.email],
            html_message=message_html,
            fail_silently=False,
        )
        return True
    except Exception as e:
        print(f"Erreur d'envoi d'email : {e}")
        return False


def envoyer_rappel_evenement(evenement):
    """
    Envoie un rappel aux participants 24h avant l'événement
    """
    inscrits = evenement.inscriptions.filter(statut='confirmee')
    
    if not inscrits.exists():
        return False
    
    sujet = f"⏰ Rappel - {evenement.titre} demain"
    
    emails = []
    for inscription in inscrits:
        participant = inscription.participant
        
        message_html = f"""
        <html>
            <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
                <div style="max-width: 600px; margin: 0 auto; padding: 20px; border: 1px solid #ddd; border-radius: 10px;">
                    <h2 style="color: #f59e0b;">⏰ Rappel : Événement demain !</h2>
                    
                    <p>Bonjour <strong>{participant.get_full_name()}</strong>,</p>
                    
                    <p>Nous vous rappelons que l'événement suivant aura lieu <strong>demain</strong> :</p>
                    
                    <div style="background: #fffbeb; padding: 15px; border-radius: 8px; margin: 20px 0;">
                        <h3 style="margin-top: 0; color: #f59e0b;">{evenement.titre}</h3>
                        <p><strong>📅 Date :</strong> {evenement.date_debut.strftime('%d/%m/%Y à %H:%M')}</p>
                        <p><strong>📍 Lieu :</strong> {evenement.lieu}</p>
                        <p><strong>👤 Organisateur :</strong> {evenement.organisateur.get_full_name()}</p>
                    </div>
                    
                    <p><strong>⚠️ N'oubliez pas :</strong></p>
                    <ul>
                        <li>Arrivez à l'heure</li>
                        <li>Préparez vos questions si nécessaire</li>
                        <li>En cas d'empêchement, annulez votre inscription</li>
                    </ul>
                    
                    <p style="margin-top: 30px;">À demain !</p>
                </div>
            </body>
        </html>
        """
        
        message_texte = strip_tags(message_html)
        
        emails.append((
            sujet,
            message_texte,
            settings.DEFAULT_FROM_EMAIL,
            [participant.email],
        ))
    
    try:
        send_mass_mail(emails, fail_silently=False)
        return True
    except Exception as e:
        print(f"Erreur d'envoi d'emails : {e}")
        return False