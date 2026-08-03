from django.core.management.base import BaseCommand
from apps.kinglife.models import Service, CategorieProduit, Article, Actualite, Realisation, Page


class Command(BaseCommand):
    help = 'Alimente la base de données avec des informations réelles et complètes pour KINGLIFE SARL U'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS("Début du peuplement des données KINGLIFE SARL U..."))

        # 1. PEUPLEMENT DES 12 SERVICES MARITIMES
        services_data = [
            {
                'nom': 'General Trade & Négoce International',
                'categorie': 'general_trade',
                'description': 'Fourniture et approvisionnement général de marchandises, matériel commercial et consommables industriels pour les entreprises maritimes et terrestres à Port-Gentil et sur la côte ouest-africaine.',
                'icone': '📦',
                'ordre': 1
            },
            {
                'nom': 'Import – Export & Logistique Internationale',
                'categorie': 'import_export',
                'description': 'Gestion complète des procédures douanières d’importation et d’exportation de fret marchandise, suivi de conteneurs et dédouanement express en zone portuaire.',
                'icone': '🌐',
                'ordre': 2
            },
            {
                'nom': 'Ship Chandler (Avitaillement Maritime)',
                'categorie': 'ship_chandler',
                'description': 'Approvisionnement complet des navires en vivres frais, congelés et secs, eau douce potable, matériels de sécurité, EPI et fournitures de pont et machines.',
                'icone': '🚢',
                'ordre': 3
            },
            {
                'nom': 'Shipping Agency & Consignation de Navires',
                'categorie': 'shipping_agency',
                'description': 'Assistance 24/7 aux armateurs et capitaines lors des escales portuaires : formalités administratives, pilotage, remorquage, démarches douanières et assistance d’urgence.',
                'icone': '⚓',
                'ordre': 4
            },
            {
                'nom': 'Transit & Commission de Transport',
                'categorie': 'transit',
                'description': 'Acheminement sécurisé de colis lourds, pièces de rechange navales et marchandises par voie terrestre, maritime et aérienne avec suivi logistique en temps réel.',
                'icone': '🚛',
                'ordre': 5
            },
            {
                'nom': 'Crew Change (Relève d\'Équipage)',
                'categorie': 'crew_change',
                'description': 'Prise en charge intégrale de la relève des marins et officiers : visas d’escale, accueil à l’aéroport, transferts sécurisés, hébergement et embarquement à bord.',
                'icone': '👥',
                'ordre': 6
            },
            {
                'nom': 'Offshore Services & Assistance Plateformes',
                'categorie': 'offshore',
                'description': 'Support logistique et technique aux bateaux de soutien (PSV/AHTS) et plateformes pétrolières offshore : transfert de matériel, ravitaillement et assistance technique.',
                'icone': '🏗️',
                'ordre': 7
            },
            {
                'nom': 'Bunker Supply (Ravitaillement en Carburant)',
                'categorie': 'bunker',
                'description': 'Livraison de fioul marin (MGO, IFO 380 Low Sulfur) par barge ou camion-citerne en rade et à quai selon les normes internationales ISO 8217.',
                'icone': '⛽',
                'ordre': 8
            },
            {
                'nom': 'Lubricant Supply (Huiles & Lubrifiants Marins)',
                'categorie': 'lubricant',
                'description': 'Distribution d’huiles moteur marine haute performance, graisses spéciales et liquides de refroidissement certifiés pour moteurs principaux et auxiliaires.',
                'icone': '🛢️',
                'ordre': 9
            },
            {
                'nom': 'Sludge Removal (Traitement des Boues & Hydrocarbures)',
                'categorie': 'sludge',
                'description': 'Pompage, collecte et acheminement vers les centres de traitement agréés des eaux usées de cale et résidus d’hydrocarbures conformément aux conventions MARPOL.',
                'icone': '♻️',
                'ordre': 10
            },
            {
                'nom': 'Garbage Removal (Gestion des Déchets Maritimes)',
                'categorie': 'garbage',
                'description': 'Service d’évacuation et de tri des déchets solides et organiques des navires en escale avec délivrance d’un certificat d’élimination écologique.',
                'icone': '🗑️',
                'ordre': 11
            },
            {
                'nom': 'Shipping Maintenance & Réparation Navale',
                'categorie': 'maintenance',
                'description': 'Interventions techniques d’urgence et maintenance préventive : travaux de soudure, chaudronnerie, électricité marine et révision d’équipements de sécurité.',
                'icone': '🔧',
                'ordre': 12
            },
        ]

        for s_data in services_data:
            Service.objects.update_or_create(
                categorie=s_data['categorie'],
                defaults=s_data
            )
        self.stdout.write(self.style.SUCCESS("[OK] 12 Services Maritimes crees/mis a jour avec succes."))

        # 2. PEUPLEMENT DES PAGES INSTITUTIONNELLES
        pages_data = [
            {
                'slug': 'historique',
                'titre': 'Notre Historique',
                'contenu': 'Fondée à Port-Gentil, KINGLIFE SARL U s’est rapidement développée pour devenir un acteur incontournable des services maritimes et logistiques au Gabon et dans le Golfe de Guinée. Grâce à la rigueur de sa chaîne logistique et à son expertise en avitaillement et transit, l’entreprise a su bâtir des partenariats durables avec de grands armateurs et opérateurs offshore internationaux.'
            },
            {
                'slug': 'mission',
                'titre': 'Notre Mission',
                'contenu': 'Fournir des solutions maritimes, logistiques et d’avitaillement d’une fiabilité absolue, disponibles 24h/24 et 7j/7, garantissant ainsi la continuité opérationnelle des navires et des plateformes en toute sécurité.'
            },
            {
                'slug': 'vision',
                'titre': 'Notre Vision',
                'contenu': 'Être le partenaire maritime d’excellence le plus innovant et réactif de la région, reconnu pour ses standards de sécurité élevés et la digitalisation complète de ses processus commerciaux et de suivi.'
            },
            {
                'slug': 'valeurs',
                'titre': 'Nos Valeurs',
                'contenu': '• Excellence & Réactivité : Réponse immédiate aux exigences maritimes.\n• Sécurité & Conformité : Respect strict des règles MARPOL et SOLAS.\n• Intégrité & Transparence : Relations de confiance avec nos armateurs et partenaires.'
            },
        ]

        for p_data in pages_data:
            Page.objects.update_or_create(
                slug=p_data['slug'],
                defaults=p_data
            )
        self.stdout.write(self.style.SUCCESS("[OK] Pages institutionnelles creees/mises a jour."))

        # 3. PEUPLEMENT DES CATÉGORIES ET ARTICLES DE CATALOGUE
        categories_data = [
            {'nom': 'Ship Chandler - Vivres & Provisions', 'description': 'Alimentation fraîche, congelée et boissons pour équipages.', 'ordre': 1},
            {'nom': 'Bunker & Carburants Marins', 'description': 'MGO, IFO 380 et fioul marin certifié.', 'ordre': 2},
            {'nom': 'Huiles & Lubrifiants', 'description': 'Huiles moteur et graisses marines haute pression.', 'ordre': 3},
            {'nom': 'Équipements de Sécurité & Pont', 'description': 'EPI, extincteurs, cordages et outillage de bord.', 'ordre': 4},
        ]

        cat_objs = {}
        for c_data in categories_data:
            cat_obj, _ = CategorieProduit.objects.update_or_create(
                nom=c_data['nom'],
                defaults=c_data
            )
            cat_objs[c_data['nom']] = cat_obj

        articles_data = [
            {'nom': 'Eau Douce Potable (Litre / Tonne)', 'categorie': cat_objs['Ship Chandler - Vivres & Provisions'], 'description': 'Eau potable certifiée pour avitaillement des cuves de navire.', 'prix_unitaire': 15.00, 'unite': 'Tonne'},
            {'nom': 'Pack Vivres Frais Équipage (10 Marins / Semaine)', 'categorie': cat_objs['Ship Chandler - Vivres & Provisions'], 'description': 'Légumes frais, viandes, poissons et produits de boulangerie.', 'prix_unitaire': 1200.00, 'unite': 'Pack'},
            {'nom': 'Marine Gas Oil (MGO Low Sulfur)', 'categorie': cat_objs['Bunker & Carburants Marins'], 'description': 'Carburant marin basse teneur en soufre conforme ISO 8217.', 'prix_unitaire': 850.00, 'unite': 'Tonne'},
            {'nom': 'Huile Moteur Marine SAE 40 (Fût 208L)', 'categorie': cat_objs['Huiles & Lubrifiants'], 'description': 'Huile haute qualité pour moteurs diesel marins de forte puissance.', 'prix_unitaire': 450.00, 'unite': 'Fût'},
            {'nom': 'Gilet de Sauvetage Homologué SOLAS', 'categorie': cat_objs['Équipements de Sécurité & Pont'], 'description': 'Gilet de sauvetage 150N avec lampe torche automatique.', 'prix_unitaire': 65.00, 'unite': 'Unité'},
        ]

        for a_data in articles_data:
            Article.objects.update_or_create(
                nom=a_data['nom'],
                defaults=a_data
            )
        self.stdout.write(self.style.SUCCESS("[OK] Categories et Articles du catalogue initialises."))

        # 4. ACTUALITÉS & RÉALISATIONS
        Actualite.objects.get_or_create(
            titre="Excellence opérationnelle : Nouveau service d'avitaillement haute capacité",
            defaults={
                'contenu': "KINGLIFE SARL U renforce sa flotte de barges pour le ravitaillement rapide des navires cargo et pétroliers en rade au large de Port-Gentil. Ce nouveau service permet de réduire de 40% le temps d'escale.",
                'resume': "Renforcement de notre flotte de barges pour un avitaillement ultra-rapide des navires.",
            }
        )
        Actualite.objects.get_or_create(
            titre="Obtention des accréditations de sûreté et normes environnementales ISO",
            defaults={
                'contenu': "Confirmation de la conformité de nos protocoles maritimes aux meilleures exigences de sécurité environnementale ISO 14001 et gestion des déchets MARPOL.",
                'resume': "Validation de la conformité aux exigences environnementales maritimes.",
            }
        )

        Realisation.objects.get_or_create(
            titre="Avitaillement Pétrolier Haute Mer",
            defaults={
                'description': "Opération d'avitaillement vivres et eau douce pour un navire pétrolier de 200 000 tonnes en rade de Port-Gentil.",
                'date_realisation': '2024-05-15',
                'client': 'Armateur International'
            }
        )

        self.stdout.write(self.style.SUCCESS("Peuplement complet termine avec succes !"))
