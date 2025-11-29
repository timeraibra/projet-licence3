"""
Configuration des URLs du projet gestion_evenements
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('evenements.urls')),  # IMPORTANT: Cette ligne doit être présente
]

# Servir les fichiers media en développement
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# Personnalisation de l'admin
admin.site.site_header = "Administration - Événements Universitaires"
admin.site.site_title = "Gestion d'Événements"
admin.site.index_title = "Tableau de bord administrateur"