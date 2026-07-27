-- ==========================================================================
-- SCRIPT DE NETTOYAGE — À EXÉCUTER DANS SUPABASE SQL EDITOR
-- Supprime TOUTES les tables pour laisser Django les recréer proprement
-- ==========================================================================

-- Supprimer toutes les tables existantes (avec CASCADE pour les dépendances)
DROP TABLE IF EXISTS
    kinglife_paiement,
    kinglife_facture,
    kinglife_prestation,
    kinglife_cotation,
    kinglife_lignecotation,
    kinglife_demandecotation,
    kinglife_contact,
    kinglife_realisation,
    kinglife_actualite,
    kinglife_article,
    kinglife_categorieproduit,
    kinglife_service,
    kinglife_page,
    django_admin_log,
    django_session,
    auth_user_user_permissions,
    auth_user_groups,
    auth_group_permissions,
    auth_permission,
    auth_group,
    auth_user,
    django_content_type,
    django_migrations
CASCADE;

-- Vérification : doit retourner 0 tables
SELECT COUNT(*) as tables_restantes
FROM information_schema.tables
WHERE table_schema = 'public'
  AND table_name LIKE ANY(ARRAY['kinglife_%', 'auth_%', 'django_%']);
