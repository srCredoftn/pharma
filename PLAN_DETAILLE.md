# 🏥 PLAN DÉTAILLÉ – Pharmacie Camp Guézo (Laravel 11)

## 📋 Vue d'ensemble
- **Durée estimée** : 12-16 semaines (full stack)
- **Tech Stack** : Laravel 11, PostgreSQL, Redis, Meilisearch, Filament PHP 3
- **Locale** : fr-BJ, Fuseau : Africa/Porto-Novo, Devise : XOF
- **Environnement** : Local (Docker/Sail), Staging, Production

---

## 🎯 PHASE 0 : SETUP & ARCHITECTURE (Semaine 1)

### 0.1 Initialisation du projet
- [ ] Créer projet Laravel 11 avec `laravel new pharmacie`
- [ ] Configurer `.env` :
  - `APP_NAME=Pharmacie Camp Guézo`
  - `APP_LOCALE=fr_BJ`
  - `APP_TIMEZONE=Africa/Porto-Novo`
  - `DB_CONNECTION=pgsql` (PostgreSQL)
  - Clés paiement (vides pour l'instant)
- [ ] Setup Docker / Laravel Sail (compose.yml avec PostgreSQL + Redis)
- [ ] Initialiser Git + `.gitignore`

### 0.2 Dépendances essentielles
```bash
composer require laravel/breeze
composer require spatie/laravel-permission
composer require spatie/laravel-media-library
composer require filament/filament --with=forms --with=notifications --with=tables
composer require laravel/scout
composer require meilisearch/meilisearch-php
composer require stripe/stripe-php
composer require laravel/cashier-stripe (optionnel, paiements)
composer require barryvdh/laravel-dompdf
composer require intervention/image
composer require laravel/horizon
```

### 0.3 Architecture des dossiers
```
app/
├── Http/
│   ├── Controllers/
│   │   ├── Admin/ (Dashboard & gestion)
│   │   ├── Api/V1/ (Endpoints API)
│   │   └── Web/ (Frontend client)
│   ├── Requests/ (Form requests + validation)
│   ├── Resources/ (API resources)
│   └── Middleware/
├── Models/ (Eloquent models)
├── Services/ (Métier complexe)
├── Actions/ (Actions réutilisables)
├── Payments/ (Abstraction paiements)
├── Notifications/ (Mailables)
├── Policies/ (Autorisation)
├── Enums/ (Statuts, rôles)
└── Exceptions/

routes/
├── web.php (Frontend)
├── api.php (API v1)
├── admin.php (Dashboard Filament)
└── channels.php

resources/
├── views/ (Blade templates)
├── js/ (Assets frontend)
└── css/ (Styles)

database/
├── migrations/
├── seeders/
└── factories/

storage/
├── app/prescriptions/ (Ordonnances)
└── app/products/ (Images produits)

config/
├── settings.php (Config locale: XOF, taxes, zones)
├── payment-providers.php
└── media-library.php
```

### 0.4 Configuration locale Bénin
- [ ] Créer `config/benin.php` :
  - Devise XOF, symbole, format numérique (virgule décimale)
  - Fuseau Africa/Porto-Novo
  - Locale fr_BJ
  - Taux TVA (20% défaut, variable par produit)
  - Zones livraison (Cotonou, Abomey-Calavi, Porto-Novo, etc.)
  - Contacts (tél, email)
- [ ] Ajouter locales **fr_BJ** dans `lang/fr_BJ/` (messages, validation)
- [ ] Configurer `Locale::setFallback('fr')` dans AppServiceProvider

### 0.5 Seeding initial
- [ ] Créer DatabaseSeeder :
  - Admin user (test@pharmacie.test, password)
  - Rôles (admin, pharmacien, client)
  - Permissions CRUD (articles, produits, commandes, ordonnances, etc.)
- [ ] Lancer migrations + seeding

### 0.6 Sécurité de base
- [ ] Configurer `config/app.php`, `config/database.php` pour prod-ready
- [ ] Setup CORS dans `config/cors.php` (API)
- [ ] Headers sécurité (CSP, HSTS) via `Http/Middleware/SecurityHeaders`
- [ ] Rate limiting (API throttle)

**✅ Livrables Phase 0** :
- Projet Laravel initialisé, DB prête, dépendances installées
- Structure de dossiers professionnelle
- Seeder test (admin, rôles, permissions)

---

## 🎯 PHASE 1 : MODÈLES & AUTHENTIFICATION (Semaine 2)

### 1.1 Modèles & Migrations
#### Users & Auth
- [ ] **Migration** `create_users_table` (id, name, email, email_verified_at, password, phone, avatar, is_active, created_at)
- [ ] **Model User** + relations (HasMany orders, prescriptions, addresses, appointments)
- [ ] **Enum Role** : ADMIN, PHARMACIST, CLIENT

#### Rôles & Permissions (Spatie)
- [ ] **Migration** via spatie/laravel-permission (roles, permissions, model_has_roles, etc.)
- [ ] **Seeder** : Permissions CRUD (manage_products, manage_categories, manage_users, manage_prescriptions, manage_orders, etc.)
- [ ] **Rôles** :
  - Admin : toutes permissions
  - Pharmacien : manage_prescriptions, view_orders, view_analytics
  - Client : view_products, manage_own_orders, upload_prescriptions

#### Adresses
- [ ] **Model Address** (user_id, order_id, type{billing,shipping}, first_name, last_name, address1, address2, zip, city, country, phone)
- [ ] Validation : masque tel +229 (Bénin)

### 1.2 Authentification avec Laravel Breeze
- [ ] Installer Breeze (Blade)
  ```bash
  php artisan breeze:install --views
  ```
- [ ] Customiser templates (login, register, reset password) avec branding Pharmacie Camp Guézo
- [ ] Email verification obligatoire
- [ ] Redirect post-login selon rôle (admin → dashboard Filament, client → catalogue)

### 1.3 API Tokens (Sanctum)
- [ ] Configurer Sanctum dans `config/sanctum.php`
- [ ] Migrer `create_personal_access_tokens_table`
- [ ] Routes API : `POST /api/v1/auth/login`, `POST /logout`, `GET /me`
- [ ] Middleware `auth:sanctum` pour routes protégées

### 1.4 Politiques (Policies)
- [ ] **UserPolicy** : update own profile, view own orders
- [ ] **OrderPolicy** : view own orders (client), manage all (admin)
- [ ] **PrescriptionPolicy** : upload own (client), view all + manage (pharmacien/admin)
- [ ] **ProductPolicy** : view published (public), manage (admin)

### 1.5 Énumérations
- [ ] `Enums/OrderStatus.php` : DRAFT, PENDING_PAYMENT, PAID, PROCESSING, SHIPPED, DELIVERED, CANCELED
- [ ] `Enums/PaymentStatus.php` : PENDING, SUCCESSFUL, FAILED, REFUNDED
- [ ] `Enums/PrescriptionStatus.php` : RECEIVED, VALIDATED, REJECTED, PROCESSED
- [ ] `Enums/ShipmentStatus.php` : PENDING, SHIPPED, IN_TRANSIT, DELIVERED

**✅ Livrables Phase 1** :
- Tous modèles & migrations en place
- Auth (register/login/reset password) fonctionnelle
- Rôles & permissions configurés
- Policies en place (tests unitaires)

---

## 🎯 PHASE 2 : CATALOGUE PRODUITS (Semaine 3-4)

### 2.1 Modèles Catalogue
#### Marques
- [ ] **Model Brand** (id, name, slug, description, logo, is_active)
- [ ] Slug auto-généré via `Illuminate\Support\Str::slug()`
- [ ] Relation HasMany → products

#### Catégories
- [ ] **Model Category** (id, name, slug, parent_id, depth, description, is_active, image, path)
- [ ] Arborescence hiérarchique jusqu'à 4 niveaux
- [ ] Self-referencing relation (belongsTo parent, hasMany children)
- [ ] Cache de l'arborescence (Redis)

#### Produits
- [ ] **Model Product** (id, name, slug, brand_id, short_desc, long_desc, sku, ean, price_ht, price_ttc, tax_rate, stock, is_active, published_at)
- [ ] Relations :
  - BelongsTo Brand
  - BelongsToMany Category (pivot table product_category)
  - HasMany Media (via spatie/laravel-media-library)
- [ ] Scopes : `published()`, `inStock()`, `byCategory()`, `byBrand()`

#### Médias (Images)
- [ ] **Configurer spatie/laravel-media-library** :
  - Collection `gallery` (images produits)
  - Conversions responsive (thumbnail 300x300, medium 600x600, large 1200x1200)
  - Disk `products` (storage/app/products)
- [ ] **Model Media** migré automatiquement

### 2.2 Recherche Fulltext (Meilisearch + Scout)
- [ ] Setup Meilisearch (Docker container ou service externe)
- [ ] Configurer `config/scout.php` (driver=meilisearch)
- [ ] **Model Product** implémente `Searchable`
- [ ] Index **products** avec attributes : name, sku, ean, brand.name, categories.name
- [ ] Filterable attributes : brand_id, category_id, price_ttc, stock
- [ ] Synchronisation via `php artisan scout:sync-index-settings`

### 2.3 Contrôleurs & Routes Catalogue
#### API Endpoints
- [ ] **ProductController** :
  - `GET /api/v1/products` (listing avec filtres, tri, pagination)
  - `GET /api/v1/products/{slug}` (détail)
  - `GET /api/v1/search?q=...` (fulltext)
  - `GET /api/v1/search/autocomplete?q=...` (<150ms p95)
  
- [ ] **CategoryController** :
  - `GET /api/v1/categories` (liste complète, arborescence)
  - `GET /api/v1/categories/{slug}` (détail + produits)
  
- [ ] **BrandController** :
  - `GET /api/v1/brands` (liste)
  - `GET /api/v1/brands/{slug}` (détail + produits)

#### Validation & Requests
- [ ] `ProductFilterRequest` (page, per_page, category, brand, price_min, price_max, sort, search)
- [ ] Server-side validation

### 2.4 Frontend Catalogue (Blade)
- [ ] Layout principal (header, nav, footer)
- [ ] **Pages** :
  - Accueil (hero, catégories, top produits)
  - Listing produits par catégorie (filtres sidebar, pagination)
  - Page produit détail (galerie, description, prix, stock, ajouter panier)
  - Recherche résultats
  - Pages marques
- [ ] CSS responsive (TailwindCSS ou Bootstrap)

### 2.5 Admin : Gestion Catalogue (Filament)
- [ ] **Ressources Filament** :
  - ProductResource (CRUD, images, catégories, prix)
  - CategoryResource (CRUD hiérarchique)
  - BrandResource (CRUD, logo)
- [ ] Listes avec filtres (statut, stock, catégorie, marque)
- [ ] Tri (prix, stock, date création)
- [ ] Actions bulk (publish, archive, supprimer)

**✅ Livrables Phase 2** :
- Catalogue complet (marques, catégories, produits, médias)
- Recherche fulltext rapide (<150ms)
- Frontend catalogue fonctionnel
- Admin Filament pour gestion catalogue

---

## 🎯 PHASE 3 : PANIER & CHECKOUT (Semaine 5)

### 3.1 Modèles Panier
#### Cart
- [ ] **Model Cart** (id, user_id|null, session_id, currency=XOF, coupon_code|null, subtotal, tax_total, shipping_total, grand_total)
- [ ] Relations HasMany cart_items
- [ ] Scope `active()` pour panier courant

#### CartItem
- [ ] **Model CartItem** (id, cart_id, product_id, quantity, unit_price, total)
- [ ] Calcul auto du total (quantity × unit_price)
- [ ] Validation stock à l'ajout

### 3.2 Logique Panier (Service)
- [ ] **Service CartService** :
  - `addToCart(product, quantity)`
  - `updateItem(cartItem, quantity)` + validation stock
  - `removeItem(cartItem)`
  - `clearCart()`
  - `getOrCreateCart()` (invité + user)
  - Calcul sous-total, taxes, frais livraison
- [ ] Middleware `syncCartToUser` (invité → user après login, fusion panier)
- [ ] Persistance session (invités via session_id)

### 3.3 Commandes
#### Order
- [ ] **Model Order** (id, user_id, number unique, status, currency=XOF, subtotal, tax_total, shipping_total, discount_total, grand_total, paid_at|null, created_at)
- [ ] Relations :
  - BelongsTo user
  - HasMany order_items
  - HasOne address (shipping)
  - HasOne payment
  - HasOne shipment
  - HasMany prescriptions (optionnel, post-achat)

#### OrderItem
- [ ] **Model OrderItem** (id, order_id, product_id, name, sku, unit_price, quantity, total, tax_rate)

#### OrderAddress
- [ ] **Model OrderAddress** (order_id, type{billing,shipping}, first_name, last_name, address1, address2, zip, city, country, phone)

### 3.4 Checkout Flow
- [ ] **CheckoutController** :
  - `GET /checkout` → formulaire adresse (billing/shipping), mode livraison
  - `POST /checkout` → validation, création order DRAFT, réservation stock
  - `GET /checkout/payment` → sélection moyen paiement, redirection provider

#### Validation Checkout
- [ ] `CheckoutRequest` (validations address, téléphone +229, code postal Bénin)
- [ ] Vérification stock temps réel
- [ ] Calcul frais livraison selon zone

### 3.5 API Panier
- [ ] `GET /api/v1/cart` (détail + items)
- [ ] `POST /api/v1/cart/items` (add)
- [ ] `PATCH /api/v1/cart/items/{id}` (update quantity)
- [ ] `DELETE /api/v1/cart/items/{id}` (remove)
- [ ] `POST /api/v1/checkout` (create order)

### 3.6 Notifications
- [ ] **Mailable OrderConfirmation** (envoyé après paiement réussi)
  - Numéro commande, articles, total, lien suivi

**✅ Livrables Phase 3** :
- Panier persistant (invité + user)
- Checkout validé
- Commandes créées + numérotation
- Emails de confirmation

---

## 🎯 PHASE 4 : INTÉGRATION PAIEMENTS (Semaine 6)

### 4.1 Abstraction PaymentProvider
- [ ] **Interface PaymentProvider** :
  - `createPaymentIntent(order, amount, currency)` → intent_id
  - `confirmPayment(intent_id)` → success/failed
  - `refund(payment, amount)` → refund_id
  - `handleWebhook(payload, signature)` → validated

- [ ] **Providers implémentés** :
  - `StripeProvider` (cartes internationales)
  - `FedaPayProvider` (MTN, Moov, Celtiis, cartes)
  - `UBAProvider` (cartes UBA/locales)
  - Fallback `CinetPayProvider` (optional)

### 4.2 Configuration Paiements
- [ ] `.env` : clés sandbox pour chaque provider
  - `STRIPE_SECRET`, `STRIPE_PUBLIC`
  - `FEDAPAY_API_KEY`, `FEDAPAY_PUBLIC_KEY`
  - `UBA_MERCHANT_ID`, `UBA_API_KEY`
  - `WEBHOOK_SECRET_STRIPE`, etc.
- [ ] `config/payment-providers.php` (mapping provider → classe)

### 4.3 Modèle Payment
- [ ] **Model Payment** (id, order_id, provider{stripe|fedapay|uba}, intent_id, status{pending|successful|failed|refunded}, amount, currency, payload JSON, created_at)
- [ ] Relation BelongsTo order
- [ ] Scope `byProvider()`

### 4.4 Controllers Paiement
- [ ] **PaymentController** :
  - `POST /payments/intent` → appel provider, retour intent_id + redirect URL si nécessaire
  - `GET /payments/confirm?intent_id=...` → validation, update order → PAID
  - `POST /payments/{id}/refund` (admin) → appel provider, update payment → REFUNDED

### 4.5 Webhooks
- [ ] **WebhookController** :
  - `POST /webhooks/stripe` → vérif signature, mise à jour order/payment
  - `POST /webhooks/fedapay` → idem
  - `POST /webhooks/uba` → idem
- [ ] **Validation** :
  - Vérification signature (HMAC SHA256)
  - Idempotency (webhook_id unique)
  - Montant/devise match order
- [ ] **Actions webhook** :
  - `ChargeSuccessful` → order.status = PAID, décrement stock, envoi email
  - `ChargeFailed` → order.status = FAILED, email notification
  - `ChargeRefunded` → payment.status = REFUNDED, recréditer stock

### 4.6 Journalisation Paiements
- [ ] Table **webhooks** (id, provider, event, payload, processed_at, status)
- [ ] Logging dans channel dédié `config/logging.php` → `storage/logs/payments.log`
- [ ] Traçabilité complète (pour audit)

### 4.7 Génération Facture PDF
- [ ] **Service InvoiceService** :
  - Génération PDF via dompdf
  - Template Blade (facture.blade.php)
  - Logo Pharmacie Camp Guézo, numéro facture, items, montants
  - Sauvegarde storage/invoices/{order_number}.pdf
- [ ] Email facture attachée après paiement réussi

### 4.8 Réconciliation Quotidienne
- [ ] **Command ReconcilePayments** (cron quotidien)
  - Appel API providers pour statut paiements en attente
  - Mise à jour si changement d'état
  - Alertes admin si incohérences

**✅ Livrables Phase 4** :
- Tous providers paiement intégrés + abstraction
- Webhooks sécurisés
- Factures PDF générées
- Journalisation complète

---

## 🎯 PHASE 5 : ORDONNANCES (Semaine 7)

### 5.1 Modèle Prescription
- [ ] **Model Prescription** (id, order_id|null, user_id, status{received|validated|rejected|processed}, uploaded_by(user_id), file_path, file_disk=s3, file_name_original, uploaded_at, verified_by(user_id)|null, verified_at|null, rejected_by(user_id)|null, rejected_at|null, rejection_reason|null, notes_internal TEXT, created_at)
- [ ] Relation BelongsTo user, BelongsTo order (optionnel)
- [ ] Scopes : `pending()`, `byStatus()`, `recent()`

### 5.2 Upload Sécurisé
- [ ] **PrescriptionController** :
  - `POST /prescriptions` (formulaire upload)
  - Validation :
    - Extensions autorisées : PDF, JPG, PNG
    - Taille max 10MB
    - Scan antivirus (ClamAV optional)
  - Stockage S3/MinIO avec chiffrement SSE-S3
  - Génération filename unique (hash)
  - DB logging (user_id, timestamp)

- [ ] **Form PrescriptionRequest** :
  - `file` : required|file|mimes:pdf,jpg,jpeg,png|max:10240
  - `notes` : nullable|string|max:500

### 5.3 Workflow Pharmacien
- [ ] **Statuts** :
  - RECEIVED : ordonnance uploadée, attente validation
  - VALIDATED : pharmacien approuve
  - REJECTED : pharmacien refuse + motif
  - PROCESSED : ordonnance traitée, commande liée

- [ ] **PrescriptionService** :
  - `validate(prescription)` → statut VALIDATED, verified_by, verified_at
  - `reject(prescription, reason)` → statut REJECTED, email user
  - `markProcessed(prescription)` → statut PROCESSED

### 5.4 Dashboard Pharmacien (Filament)
- [ ] **PrescriptionResource** (Filament) :
  - Liste paginée (filtres: statut, date, utilisateur)
  - Détail : preview PDF inline (PDO ou iframe)
  - Actions :
    - View (lecture)
    - Validate (changement statut → VALIDATED)
    - Reject (modal motif)
    - Mark Processed
  - Notes internes (commentaires privés)

### 5.5 Sécurité Accès
- [ ] **Policy PrescriptionPolicy** :
  - Client : viewOwn (ses ordonnances)
  - Pharmacien : viewAll, manage
  - Admin : viewAll, manage, delete
- [ ] Routes protégées middleware `auth:sanctum` + policy check

### 5.6 Lien Ordonnance ↔ Commande
- [ ] Workflow optionnel :
  1. Client upload ordonnance AVANT achat → associée à order_id NULL
  2. Au checkout, proposer association automatique ou manuelle
  3. Ou upload APRÈS commande (lien direct order_id)
- [ ] Affichage ordonnance dans détail commande (client + pharmacien)

### 5.7 Notifications
- [ ] Email client upload confirmation
- [ ] Email pharmacien : nouvelle ordonnance en attente (pour chaque upload ou digest)
- [ ] Email client : validation/rejection (avec motif si rejet)

**✅ Livrables Phase 5** :
- Modèle ordonnances complet
- Upload sécurisé (S3, antivirus)
- Workflow pharmacien implémenté
- Dashboard Filament pharmacien
- Contrôle d'accès strict

---

## 🎯 PHASE 6 : DASHBOARD ADMIN (Semaine 8)

### 6.1 Filament Setup
- [ ] Installation & publication assets :
  ```bash
  php artisan filament:install --with=forms --with=tables --with=notifications
  php artisan vendor:publish --tag=filament-views
  ```
- [ ] Configuration `config/filament.php` (branding, locale=fr_BJ, timezone)
- [ ] Authentification Filament = Laravel auth existant

### 6.2 Ressources Filament (CRUD)
Chaque ressource : List, Create, Edit, View pages

#### ProductResource
- [ ] Champs : name, slug, brand (select), categories (multi-select), short_desc, long_desc, sku, ean, price_ht, price_ttc, tax_rate, stock, is_active, published_at
- [ ] Upload images (galerie) via media-library widget
- [ ] Filtres : statut, stock, catégorie, marque, prix
- [ ] Tri : prix, stock, date création
- [ ] Actions bulk : publish, archive, delete

#### CategoryResource
- [ ] Champs : name, slug, parent_id (select hiérarchique), depth (read-only), description, image, is_active
- [ ] Vue arborescente si possible
- [ ] Validation slug unique

#### BrandResource
- [ ] Champs : name, slug, description, logo upload, is_active
- [ ] Slug auto-généré

#### UserResource
- [ ] Champs : name, email, email_verified_at, phone, roles (multi-select), is_active
- [ ] Actions : reset password, impersonate (optionnel)
- [ ] Filtres : rôle, statut, date création

#### OrderResource
- [ ] Champs : number, user (read-only), status, currency, subtotal, tax_total, shipping_total, grand_total, paid_at, created_at
- [ ] Onglets : items (order_items), adresse livraison, paiement (statut + détails), ordonnances liées
- [ ] Filtres : statut, date, client, montant
- [ ] Actions : marquer expédié, télécharger facture PDF

#### PrescriptionResource
- [ ] Champs : id, user, status, uploaded_at, verified_at
- [ ] Onglets : détail, preview fichier PDF, notes internes, historique changements statut
- [ ] Filtres : statut, date, utilisateur
- [ ] Actions : validate, reject (modal motif), mark processed

#### ArticleResource
- [ ] Champs : title, slug, type (news/advice), excerpt, content (WYSIWYG), cover image, tags, categories, author, status, published_at
- [ ] Éditeur richtext (Tiptap recommandé)
- [ ] Filtres : type, statut, date

#### SettingsResource
- [ ] Champs clés : company_name, phone, email, logo, hero_image, taxes_rates JSON, shipping_zones JSON
- [ ] Formulaire unique (pas de CRUD items individuels)

### 6.3 Dashboard (Accueil Admin)
- [ ] **Cartes KPI** (nombres) :
  - Total ventes (semaine/mois/année)
  - Commandes en attente
  - Ordonnances en attente
  - Clients actifs
  - Ruptures stock (alerts)

- [ ] **Graphiques** (Chart.js ou ApexCharts) :
  - Ventes par jour (7j dernier)
  - Commandes par statut (pie)
  - Produits top 10 (bar)
  - Panier moyen évolution

- [ ] **Widgets** :
  - Ordonnances récentes (dernières 5)
  - Commandes non payées
  - Stock faible (< 5 unités)

### 6.4 Statistiques & Analytics
- [ ] **Service StatsService** :
  - `getTotalRevenue(period)` (semaine/mois/année)
  - `getOrdersCount(status)`
  - `getAverageCartValue()`
  - `getTopProducts(limit=10)`
  - `getLowStockProducts(threshold=5)`

- [ ] Caching (Redis) pour perf, TTL 1h

### 6.5 Middleware & Autorisation Admin
- [ ] Middleware `AdminCheckMiddleware` sur routes /admin
- [ ] Redirection non-admin vers home
- [ ] Policy checks implicites Filament

### 6.6 Logs & Audit
- [ ] Filament Activity Log integration (spatie/laravel-activity-log optionnel)
- [ ] Traçage actions admin sensibles (create/update/delete) → logs

**✅ Livrables Phase 6** :
- Dashboard Filament complet
- Ressources CRUD productives
- KPI & graphiques
- Autorisation stricte

---

## 🎯 PHASE 7 : CONTENUS & RENDEZ-VOUS (Semaine 9)

### 7.1 Articles (Actualités / Conseils)
- [ ] **Model Post** (id, type{news|advice}, title, slug, excerpt, content, cover_media_id, tags, categories, author_id, status{draft|published}, published_at, created_at, updated_at)
- [ ] Relations :
  - BelongsTo author (user)
  - HasMany media (cover)
  - BelongsToMany Category (articles_categories pivot)
  - BelongsToMany Tag (articles_tags pivot)

#### Éditeur Richtext
- [ ] Tiptap (JavaScript editor) ou EditorJS côté admin Filament
- [ ] Sanitation HTML (purifier) côté backend
- [ ] Support images, vidéos embeds, liens

### 7.2 Frontend Articles
- [ ] **Pages** :
  - Listing articles (pagination 12/page, filtres type/catégorie/date)
  - Détail article (contenu, auteur, articles connexes, comments optionnel)
  - Catégories articles
  - Archive/recherche articles
  - Fil RSS (RFC 2822)

### 7.3 RSS Feeds
- [ ] Routes :
  - `/rss/news` → articles type=news triés date DESC
  - `/rss/advice` → articles type=advice
- [ ] Format Atom/RSS2 standard (xml)
- [ ] Library : `spatie/laravel-feed` optionnel

### 7.4 Rendez-vous (Appointments)
- [ ] **Model Appointment** (id, user_id, service_type{consultation|delivery|other}, starts_at, ends_at, notes_user, notes_admin, status{pending|confirmed|completed|canceled}, created_at)

#### Service Appointment
- [ ] Récupération créneaux libres (optionnel, intégration Google Calendar future)
- [ ] Confirmation auto par email

#### Frontend
- [ ] Formulaire prise RDV (type service, date, heure, notes)
- [ ] Validation : date > aujourd'hui, heure entre 08h-18h
- [ ] Confirmation email + rappel (24h avant via queue)

#### Admin
- [ ] Liste RDV (filtres statut, date, service)
- [ ] Détail RDV → marquer confirmé/complété/annulé
- [ ] Prise de notes admin

### 7.5 Notifications Email
- [ ] **Mailables** :
  - `AppointmentConfirmation` (client)
  - `AppointmentReminder` (24h avant)
  - `NewArticlePublished` (newsletter optionnel)
  - `PrescriptionStatusChanged`

- [ ] **Queues** :
  - QUEUE_DRIVER=redis (production)
  - Horizon pour monitoring
  - Retry policy (3 tentatives, délai exponentiel)

**✅ Livrables Phase 7** :
- Articles complets avec éditeur
- RSS feeds fonctionnels
- Rendez-vous implémentés
- Notifications email robustes

---

## 🎯 PHASE 8 : LIVRAISON, SEO, RGPD (Semaine 10)

### 8.1 Livraison
#### Modèles
- [ ] **Model ShippingZone** (id, name, cities JSON, min_weight, max_weight, base_cost, per_kg_cost, min_order_for_free)
- [ ] **Model Shipment** (id, order_id, carrier, tracking_number, tracking_url, status{pending|shipped|in_transit|delivered}, shipped_at, delivered_at)

#### Calcul Frais Livraison
- [ ] **Service ShippingService** :
  - `calculateShippingCost(zone, weight, order_amount)` → cost XOF
  - Zones Bénin : Cotonou, Abomey-Calavi, Porto-Novo, etc.
  - Logique : base_cost + weight_cost, réduction si montant > threshold

#### Suivi Colis
- [ ] Admin crée shipment après paiement accepté
- [ ] Champs carrier, tracking_number, tracking_url
- [ ] Email client avec lien suivi

### 8.2 SEO
#### Métadonnées
- [ ] Blade helper `seo($title, $description, $keywords, $image)`
- [ ] Meta tags : og:title, og:description, og:image, twitter:card
- [ ] Locale & hreflang (fr-BJ)

#### Sitemaps
- [ ] Routes :
  - `GET /sitemap.xml` → index
  - `GET /sitemap-products.xml`
  - `GET /sitemap-categories.xml`
  - `GET /sitemap-articles.xml`
- [ ] Library `spatie/laravel-sitemap`

#### Schema.org Markup
- [ ] Product schema (name, price, availability, rating)
- [ ] Article schema (headline, datePublished, author, image)
- [ ] BreadcrumbList (catégories)
- [ ] Organization schema (contact, logo, address Cotonou)

#### Pages SEO
- [ ] Titres/descriptions uniques par page
- [ ] Mot-clé principal dans H1
- [ ] Images optimisées (alt text)
- [ ] Internal linking (articles connexes, breadcrumbs)

### 8.3 RGPD & Conformité
#### Consentement Cookies
- [ ] Cookie banner (RGPD) :
  - Statistiques (Google Analytics optionnel)
  - Publicités (pixel Facebook optionnel)
  - Préférences locales browser

#### Politique de Confidentialité
- [ ] Page `/confidentialite` :
  - Données collectées
  - Durée conservation (commandes 7 ans, panier 6 mois, logs 1 an)
  - Droit accès/suppression/opposition
  - Contact DPO (optionnel)

#### Droit d'Accès/Suppression
- [ ] Endpoint API `GET /api/v1/user/data` (export JSON)
- [ ] Endpoint API `DELETE /api/v1/user/account` (anonymisation)

#### Mentions Légales
- [ ] Page `/mentions-legales` :
  - Raison sociale, adresse Cotonou, RCS
  - Directeur publication
  - Hébergeur
  - Propriété intellectuelle

#### Consentement Ordonnances
- [ ] Checkbox acceptation stockage ordonnances
- [ ] Infos de rétention légale

### 8.4 Performance
#### Caching
- [ ] Config cache (Redis) :
  - Catégories (TTL 24h)
  - Produits publiés (TTL 12h)
  - Articles (TTL 24h)
  - Settings (TTL 1h)

- [ ] HTTP Caching : ETag/Last-Modified pour API catalogue

#### Optimisation Images
- [ ] Conversion responsive (spatie/laravel-media-library)
- [ ] WebP generation (optionnel)
- [ ] Lazy loading

#### CDN
- [ ] Configuration S3 CloudFront (optionnel, prod)

**✅ Livrables Phase 8** :
- Livraison : zones, tarifs, suivi
- SEO complet (sitemap, schema, metas)
- RGPD implémenté (consentement, droits, confidentialité)
- Performance optimisée

---

## 🎯 PHASE 9 : TESTS, QA, DÉPLOIEMENT (Semaine 11-12)

### 9.1 Tests Unitaires
- [ ] Models :
  - User, Product, Order, Prescription
  - Scopes, relations, mutators
- [ ] Services :
  - CartService (add, remove, calculate)
  - PaymentService (intent, confirm)
  - ShippingService (calculate cost)
- [ ] Enums, Policies

```bash
php artisan test --filter=Unit
```

### 9.2 Tests API (Feature)
- [ ] Authentification :
  - Register, login, logout
  - Reset password
  - Sanctum tokens
  
- [ ] Catalogue :
  - GET /products (listing, filtres, pagination)
  - GET /products/{slug}
  - GET /search?q=...
  - GET /categories
  
- [ ] Panier :
  - POST /cart/items, PATCH, DELETE
  - GET /cart
  
- [ ] Paiement :
  - POST /payments/intent
  - POST /webhooks/{provider}
  - Ordonnances : POST /prescriptions, GET /prescriptions/{id}
  
- [ ] Autorisation (403 si accès non autorisé)

```bash
php artisan test --filter=Feature
```

### 9.3 Tests E2E (Optionnel Dusk)
- [ ] Scénarios utilisateur :
  - Register → Browse products → Add to cart → Checkout → Payment
  - Upload prescription → Pharmacien validation
  - Admin CRUD produits

```bash
php artisan dusk
```

### 9.4 Scan Sécurité (Semgrep)
- [ ] Vulnérabilités courantes :
  - SQL injection
  - XSS
  - CSRF token absence
  - Secrets exposés
  - Dépendances vulnérables

```bash
semgrep --config=p/security-audit --json . > semgrep-report.json
```

### 9.5 Tests de Charge
- [ ] k6 ou JMeter :
  - Catalogue : 100 concurrent users, 5min
  - Recherche : 50 users, autocomplete <150ms p95
  - Paiement webhook : 10 rps

### 9.6 QA Checklist
- [ ] Responsive mobile/tablet/desktop
- [ ] Accessibilité (WCAG 2.1 AA) :
  - Contraste couleurs
  - Alt text images
  - Navigation clavier
  - Screen reader compatibility
  
- [ ] Cross-browser (Chrome, Firefox, Safari, Edge)
- [ ] E2E scénarios critiques
- [ ] Performance (lighthouse >90)

### 9.7 Déploiement
#### Préparation
- [ ] `.env.production` :
  - Database connection (PostgreSQL managed)
  - Redis (cache/sessions)
  - S3 credentials (ordonnances, images)
  - Clés paiement production (FedaPay, UBA, Stripe)
  - Secrets (APP_KEY, JWT, etc.)

- [ ] Database migrations (prod) :
  ```bash
  php artisan migrate --force
  ```

- [ ] Seeding données initiales (marques, catégories, admin)

#### CI/CD Pipeline (GitHub Actions/GitLab CI)
- [ ] Trigger : push sur main
- [ ] Steps :
  1. Lint (PHP_CodeSniffer, Laravel Pint)
  2. Tests (phpunit)
  3. Build assets (npm run build)
  4. Security scan (Semgrep)
  5. Deploy (SSH, pull code, run migrations, cache:clear, horizon:restart)

#### Monitoring Post-Deploy
- [ ] Logs : Monolog + Sentry (erreurs)
- [ ] Performance : APM (New Relic optional)
- [ ] Uptime : Pingdom/Betterstack
- [ ] Webhooks : vérification statut (curl)

**✅ Livrables Phase 9** :
- Suite tests complète (unit, API, E2E)
- QA passée
- Déployé production
- Monitoring en place

---

## 📊 Timeline Estimée

| Phase | Titre | Durée | Jalons |
|-------|-------|-------|--------|
| 0 | Setup & Architecture | 1 semaine | Projet Laravel, DB, dépendances |
| 1 | Models & Auth | 1 semaine | Auth, rôles, permissions |
| 2 | Catalogue | 2 semaines | Produits, recherche, frontend |
| 3 | Panier & Checkout | 1 semaine | Panier, commandes, emails |
| 4 | Paiements | 1 semaine | Providers, webhooks, factures |
| 5 | Ordonnances | 1 semaine | Upload, workflow pharmacien |
| 6 | Dashboard Admin | 1 semaine | Filament, CRUD, KPI |
| 7 | Contenus & RDV | 1 semaine | Articles, RSS, appointments |
| 8 | Livraison, SEO, RGPD | 1 semaine | Zones, SEO, conformité |
| 9 | Tests, QA, Deploy | 2 semaines | Tests, sécurité, production |
| **TOTAL** | | **12-14 semaines** | MVP production-ready |

---

## 🔑 Points Critiques & Dépendances

### Dépendances Technologiques
- **PostgreSQL** : migration depuis MySQL si applicable
- **Redis** : cache, sessions, queues
- **Meilisearch** : recherche fulltext (alternative Algolia payant)
- **S3 / MinIO** : ordonnances, images
- **Clés paiement** : FedaPay, UBA, Stripe (sandbox → production)

### Risques Identifiés
1. **Sécurité ordonnances** : S3 encryption, signed URLs, access control strict
2. **Paiements webhooks** : signature validation, idempotency, reconciliation
3. **Stock** : race conditions (verrou pessimiste ou optimiste)
4. **Performance recherche** : Meilisearch indexation progressive
5. **RGPD** : droit d'accès/suppression complètement implémenté

### Priorisations
**MVP (Phase 0-5)** : Catalogue + Panier + Paiement + Ordonnances
**Complet (Phase 6-9)** : Admin full + SEO + RGPD + Tests

---

## 🛠️ Technologies Finales

```
Frontend:
├── Blade (serveur-rendu)
├── TailwindCSS / Bootstrap (styles)
├── Alpine.js (interactivité légère)
└── HTML5 (semantic)

Backend:
├── Laravel 11 (framework)
├── PostgreSQL 15+ (DB)
├── Redis (cache/sessions/queues)
├── Meilisearch (recherche)
└── S3/MinIO (fichiers)

Admin:
├── Filament PHP 3 (dashboard)
├── Tiptap / EditorJS (WYSIWYG)
├── Chart.js (graphiques)
└── spatie/laravel-* (media, permissions, etc.)

Paiements:
├── Stripe API
├── FedaPay API
└── UBA API

Déploiement:
├── Docker (local dev)
├── PostgreSQL managed (AWS RDS, Heroku, etc.)
├── S3 managed (AWS)
├── CI/CD (GitHub Actions)
└── Hosting (Heroku, Laravel Forge, DigitalOcean, etc.)

Monitoring:
├── Monolog (logs)
├── Sentry (erreurs)
├── Horizon (queues)
└── New Relic APM (optionnel)
```

---

## 📝 Notes Finales

1. **Communication Bénin** : Tous contacts, adresses, numéros téléphones en format +229 XOF
2. **Locale & Fuseau** : fr-BJ, Africa/Porto-Novo (dates, nombres)
3. **Audit & Traçabilité** : Logs complets pour ordonnances, paiements, actions admin
4. **Évolutivité** : Architecture modulaire, API versionnée, abstraction paiements
5. **Documentation** : README.md, .env.example, API docs (Swagger optionnel)

**Prêt à commencer Phase 0 ?**
