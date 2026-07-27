-- ==========================================================================
-- SCRIPT SQL COMPLET — KINGLIFE SHAL U Web Platform
-- Base de Données : Supabase (PostgreSQL)
-- Généré sur la base des modèles Django : apps/kinglife/models.py
-- ==========================================================================
-- INSTRUCTIONS :
--   1. Allez sur votre dashboard Supabase → SQL Editor
--   2. Collez ce script complet et cliquez sur "Run"
--   3. Toutes les tables seront créées automatiquement
-- ==========================================================================


-- =====================================================
-- SECTION 1 : TABLES DJANGO SYSTÈME (Auth, Sessions...)
-- =====================================================

-- Table des types de contenu (django.contrib.contenttypes)
CREATE TABLE IF NOT EXISTS django_content_type (
    id BIGSERIAL PRIMARY KEY,
    app_label VARCHAR(100) NOT NULL,
    model VARCHAR(100) NOT NULL,
    UNIQUE (app_label, model)
);

-- Table des permissions (django.contrib.auth)
CREATE TABLE IF NOT EXISTS auth_permission (
    id BIGSERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    content_type_id BIGINT NOT NULL REFERENCES django_content_type(id) ON DELETE CASCADE,
    codename VARCHAR(100) NOT NULL,
    UNIQUE (content_type_id, codename)
);

-- Table des groupes d'utilisateurs
CREATE TABLE IF NOT EXISTS auth_group (
    id BIGSERIAL PRIMARY KEY,
    name VARCHAR(150) NOT NULL UNIQUE
);

-- Permissions d'un groupe
CREATE TABLE IF NOT EXISTS auth_group_permissions (
    id BIGSERIAL PRIMARY KEY,
    group_id BIGINT NOT NULL REFERENCES auth_group(id) ON DELETE CASCADE,
    permission_id BIGINT NOT NULL REFERENCES auth_permission(id) ON DELETE CASCADE,
    UNIQUE (group_id, permission_id)
);

-- Table principale des utilisateurs Django
CREATE TABLE IF NOT EXISTS auth_user (
    id BIGSERIAL PRIMARY KEY,
    password VARCHAR(128) NOT NULL,
    last_login TIMESTAMP WITH TIME ZONE,
    is_superuser BOOLEAN NOT NULL DEFAULT FALSE,
    username VARCHAR(150) NOT NULL UNIQUE,
    first_name VARCHAR(150) NOT NULL DEFAULT '',
    last_name VARCHAR(150) NOT NULL DEFAULT '',
    email VARCHAR(254) NOT NULL DEFAULT '',
    is_staff BOOLEAN NOT NULL DEFAULT FALSE,
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    date_joined TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW()
);

-- Groupes d'un utilisateur
CREATE TABLE IF NOT EXISTS auth_user_groups (
    id BIGSERIAL PRIMARY KEY,
    user_id BIGINT NOT NULL REFERENCES auth_user(id) ON DELETE CASCADE,
    group_id BIGINT NOT NULL REFERENCES auth_group(id) ON DELETE CASCADE,
    UNIQUE (user_id, group_id)
);

-- Permissions d'un utilisateur
CREATE TABLE IF NOT EXISTS auth_user_user_permissions (
    id BIGSERIAL PRIMARY KEY,
    user_id BIGINT NOT NULL REFERENCES auth_user(id) ON DELETE CASCADE,
    permission_id BIGINT NOT NULL REFERENCES auth_permission(id) ON DELETE CASCADE,
    UNIQUE (user_id, permission_id)
);

-- Sessions Django
CREATE TABLE IF NOT EXISTS django_session (
    session_key VARCHAR(40) PRIMARY KEY,
    session_data TEXT NOT NULL,
    expire_date TIMESTAMP WITH TIME ZONE NOT NULL
);
CREATE INDEX IF NOT EXISTS django_session_expire_date ON django_session(expire_date);

-- Journal des actions d'administration (django.contrib.admin)
CREATE TABLE IF NOT EXISTS django_admin_log (
    id BIGSERIAL PRIMARY KEY,
    action_time TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    object_id TEXT,
    object_repr VARCHAR(200) NOT NULL,
    action_flag SMALLINT NOT NULL CHECK (action_flag > 0),
    change_message TEXT NOT NULL,
    content_type_id BIGINT REFERENCES django_content_type(id) ON DELETE SET NULL,
    user_id BIGINT NOT NULL REFERENCES auth_user(id) ON DELETE CASCADE
);

-- Migrations Django
CREATE TABLE IF NOT EXISTS django_migrations (
    id BIGSERIAL PRIMARY KEY,
    app VARCHAR(255) NOT NULL,
    name VARCHAR(255) NOT NULL,
    applied TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW()
);


-- =====================================================
-- SECTION 2 : TABLES MÉTIERS KINGLIFE SHAL U
-- =====================================================

-- Table : Pages du Site Institutionnel (CMS)
CREATE TABLE IF NOT EXISTS kinglife_page (
    id BIGSERIAL PRIMARY KEY,
    titre VARCHAR(200) NOT NULL,
    slug VARCHAR(50) NOT NULL UNIQUE,
    contenu TEXT NOT NULL,
    image VARCHAR(100),
    publie BOOLEAN NOT NULL DEFAULT TRUE,
    date_creation TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    date_modification TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW()
);

-- Table : Services Maritimes de KINGLIFE SHAL U
CREATE TABLE IF NOT EXISTS kinglife_service (
    id BIGSERIAL PRIMARY KEY,
    nom VARCHAR(200) NOT NULL,
    categorie VARCHAR(50) NOT NULL,
    -- Valeurs : general_trade, import_export, ship_chandler, shipping_agency,
    --           transit, crew_change, offshore, bunker, lubricant,
    --           sludge, garbage, maintenance, autre
    description TEXT NOT NULL,
    icone VARCHAR(100) NOT NULL DEFAULT '',
    image VARCHAR(100),
    ordre INTEGER NOT NULL DEFAULT 0,
    publie BOOLEAN NOT NULL DEFAULT TRUE
);
CREATE INDEX IF NOT EXISTS kinglife_service_categorie ON kinglife_service(categorie);

-- Table : Catégories de Produits du Catalogue
CREATE TABLE IF NOT EXISTS kinglife_categorieproduit (
    id BIGSERIAL PRIMARY KEY,
    nom VARCHAR(200) NOT NULL,
    description TEXT NOT NULL DEFAULT '',
    image VARCHAR(100),
    ordre INTEGER NOT NULL DEFAULT 0
);

-- Table : Articles du Catalogue
CREATE TABLE IF NOT EXISTS kinglife_article (
    id BIGSERIAL PRIMARY KEY,
    nom VARCHAR(200) NOT NULL,
    description TEXT NOT NULL,
    categorie_id BIGINT NOT NULL REFERENCES kinglife_categorieproduit(id) ON DELETE CASCADE,
    prix_unitaire NUMERIC(10, 2),
    unite VARCHAR(50) NOT NULL DEFAULT 'unité',
    image VARCHAR(100),
    stock INTEGER NOT NULL DEFAULT 0,
    publie BOOLEAN NOT NULL DEFAULT TRUE,
    date_creation TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    date_modification TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW()
);
CREATE INDEX IF NOT EXISTS kinglife_article_categorie ON kinglife_article(categorie_id);

-- Table : Actualités de l'Entreprise
CREATE TABLE IF NOT EXISTS kinglife_actualite (
    id BIGSERIAL PRIMARY KEY,
    titre VARCHAR(200) NOT NULL,
    contenu TEXT NOT NULL,
    resume VARCHAR(300) NOT NULL DEFAULT '',
    image VARCHAR(100),
    date_publication TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    publie BOOLEAN NOT NULL DEFAULT TRUE
);

-- Table : Réalisations de l'Entreprise
CREATE TABLE IF NOT EXISTS kinglife_realisation (
    id BIGSERIAL PRIMARY KEY,
    titre VARCHAR(200) NOT NULL,
    description TEXT NOT NULL,
    image VARCHAR(100) NOT NULL,
    date_realisation DATE NOT NULL,
    client VARCHAR(200) NOT NULL DEFAULT ''
);

-- Table : Messages de Contact / Demandes Clients
CREATE TABLE IF NOT EXISTS kinglife_contact (
    id BIGSERIAL PRIMARY KEY,
    nom VARCHAR(100) NOT NULL,
    email VARCHAR(254) NOT NULL,
    telephone VARCHAR(20) NOT NULL DEFAULT '',
    sujet VARCHAR(200) NOT NULL,
    message TEXT NOT NULL,
    date_envoi TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    traite BOOLEAN NOT NULL DEFAULT FALSE
);

-- Table : Demandes de Cotation des Clients
CREATE TABLE IF NOT EXISTS kinglife_demandecotation (
    id BIGSERIAL PRIMARY KEY,
    client_id BIGINT NOT NULL REFERENCES auth_user(id) ON DELETE CASCADE,
    date_demande TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    statut VARCHAR(20) NOT NULL DEFAULT 'en_attente',
    -- Valeurs : en_attente, en_cours, envoyee, acceptee, refusee, annulee
    remarques TEXT NOT NULL DEFAULT ''
);
CREATE INDEX IF NOT EXISTS kinglife_demandecotation_client ON kinglife_demandecotation(client_id);
CREATE INDEX IF NOT EXISTS kinglife_demandecotation_statut ON kinglife_demandecotation(statut);

-- Table : Lignes d'une Demande de Cotation (détail des articles)
CREATE TABLE IF NOT EXISTS kinglife_lignecotation (
    id BIGSERIAL PRIMARY KEY,
    demande_id BIGINT NOT NULL REFERENCES kinglife_demandecotation(id) ON DELETE CASCADE,
    article_id BIGINT NOT NULL REFERENCES kinglife_article(id) ON DELETE CASCADE,
    quantite INTEGER NOT NULL,
    prix_propose NUMERIC(10, 2),
    remarques TEXT NOT NULL DEFAULT ''
);
CREATE INDEX IF NOT EXISTS kinglife_lignecotation_demande ON kinglife_lignecotation(demande_id);

-- Table : Cotations Officielles (Devis du Directeur vers le Client)
CREATE TABLE IF NOT EXISTS kinglife_cotation (
    id BIGSERIAL PRIMARY KEY,
    demande_id BIGINT NOT NULL UNIQUE REFERENCES kinglife_demandecotation(id) ON DELETE CASCADE,
    numero VARCHAR(50) NOT NULL UNIQUE,
    date_creation TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    date_envoi TIMESTAMP WITH TIME ZONE,
    date_validite DATE,
    statut VARCHAR(20) NOT NULL DEFAULT 'brouillon',
    -- Valeurs : brouillon, envoyee, acceptee, refusee, expiree
    montant_total NUMERIC(12, 2) NOT NULL,
    conditions TEXT NOT NULL DEFAULT ''
);
CREATE INDEX IF NOT EXISTS kinglife_cotation_statut ON kinglife_cotation(statut);

-- Table : Prestations Maritimes (créées automatiquement après validation cotation)
CREATE TABLE IF NOT EXISTS kinglife_prestation (
    id BIGSERIAL PRIMARY KEY,
    cotation_id BIGINT REFERENCES kinglife_cotation(id) ON DELETE CASCADE,
    client_id BIGINT NOT NULL REFERENCES auth_user(id) ON DELETE CASCADE,
    titre VARCHAR(200) NOT NULL,
    description TEXT NOT NULL,
    date_debut DATE NOT NULL,
    date_fin DATE,
    statut VARCHAR(20) NOT NULL DEFAULT 'planifiee',
    -- Valeurs : planifiee, en_cours, terminee, facturee, annulee
    montant NUMERIC(12, 2) NOT NULL
);
CREATE INDEX IF NOT EXISTS kinglife_prestation_client ON kinglife_prestation(client_id);
CREATE INDEX IF NOT EXISTS kinglife_prestation_statut ON kinglife_prestation(statut);

-- Table : Factures (générées automatiquement après validation de la prestation)
CREATE TABLE IF NOT EXISTS kinglife_facture (
    id BIGSERIAL PRIMARY KEY,
    numero VARCHAR(50) NOT NULL UNIQUE,
    client_id BIGINT NOT NULL REFERENCES auth_user(id) ON DELETE CASCADE,
    prestation_id BIGINT REFERENCES kinglife_prestation(id) ON DELETE CASCADE,
    date_emission TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    date_echeance DATE NOT NULL,
    statut VARCHAR(25) NOT NULL DEFAULT 'brouillon',
    -- Valeurs : brouillon, emise, payee, partiellement_payee, annulee
    montant_ht NUMERIC(12, 2) NOT NULL,
    montant_tva NUMERIC(12, 2) NOT NULL DEFAULT 0,
    montant_ttc NUMERIC(12, 2) NOT NULL,
    montant_paye NUMERIC(12, 2) NOT NULL DEFAULT 0,
    regroupement_id BIGINT REFERENCES kinglife_facture(id) ON DELETE CASCADE
);
CREATE INDEX IF NOT EXISTS kinglife_facture_client ON kinglife_facture(client_id);
CREATE INDEX IF NOT EXISTS kinglife_facture_statut ON kinglife_facture(statut);

-- Table : Paiements Enregistrés
CREATE TABLE IF NOT EXISTS kinglife_paiement (
    id BIGSERIAL PRIMARY KEY,
    facture_id BIGINT NOT NULL REFERENCES kinglife_facture(id) ON DELETE CASCADE,
    date_paiement TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    montant NUMERIC(12, 2) NOT NULL,
    mode_paiement VARCHAR(50) NOT NULL,
    reference VARCHAR(100) NOT NULL DEFAULT ''
);
CREATE INDEX IF NOT EXISTS kinglife_paiement_facture ON kinglife_paiement(facture_id);


-- =====================================================
-- SECTION 3 : VÉRIFICATION FINALE
-- =====================================================

-- Lister toutes les tables créées pour vérification
SELECT table_name
FROM information_schema.tables
WHERE table_schema = 'public'
ORDER BY table_name;
