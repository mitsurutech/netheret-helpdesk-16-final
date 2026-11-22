# Centre d'assistance Netheret, étape 16 : version finale

[English](README.md) | [Français](README.fr.md) | [Español](README.es.md) | [日本語](README.ja.md) | [Deutsch](README.de.md)

Un exemple pour enseigner. En seize étapes, nous avons construit une application web de centre d'assistance pour Netheret, une entreprise imaginaire qui s'occupe de l'informatique de petites entreprises. Voici l'application terminée, avec son journal des modifications, ses sources et son journal de tests.

## Ce que fait l'application

| Rôle | Ce qu'il peut faire |
|------|------------------|
| Client | Créer des demandes d'assistance, suivre les demandes de son entreprise sur un fil chronologique, ajouter des commentaires, lire la base de connaissances |
| Agent Tier 1 | Trier la file, assigner et escalader les demandes, ajouter des mises à jour internes ou visibles par le client, saisir des demandes pour les clients, utiliser et rédiger la base de connaissances |
| Ingénieur Tier 2 / Tier 3 | Prendre et traiter les demandes escaladées, voir son propre planning, lire les fiches d'intervention et indiquer l'avancement |
| Responsable | Tout ce que le personnel peut faire, plus assigner à n'importe qui, planifier des interventions sur site et voir les rapports |

Chacun peut choisir un texte plus grand et un contraste élevé dans Settings.

## Lancer l'application

Il vous faut Python 3.10 ou plus récent.

```
python -m venv .venv
source .venv/bin/activate        # on Windows: .venv\Scripts\activate
pip install -r requirements.txt
python seed.py
flask --app helpdesk run --debug
```

Ouvrez http://127.0.0.1:5000. `python seed.py` efface tout et charge
des données d'exemple neuves chaque fois que vous le lancez.

### Comptes de démonstration

Ils utilisent tous le mot de passe de démonstration `password123`, réservé à ces données
d'exemple.

| Rôle | E-mail |
|------|-------|
| Responsable | `manager@netheret.example` |
| Tier 1 | `tier1@netheret.example` |
| Tier 2 | `tier2@netheret.example` |
| Tier 3 | `tier3@netheret.example` |
| Client (Brightwell Bakery) | `customer@brightwell.example` |
| Client (Harbour Dental Practice) | `customer@harbour.example` |

### Sur un vrai serveur

Définissez `SECRET_KEY` avec une longue valeur aléatoire et `SESSION_COOKIE_SECURE=1`
derrière HTTPS, et faites tourner l'application avec un serveur web de production plutôt que
`flask run`. Sans `SECRET_KEY`, l'application crée une clé aléatoire à chaque
démarrage, ce qui convient sur votre propre ordinateur.

## Organisation du code

```
requirements.txt       Flask and Flask-SQLAlchemy, pinned
seed.py                sample data (deletes everything first)
helpdesk/
  __init__.py          create_app(): settings and blueprints
  extensions.py        the db object
  models.py            the six tables and the allowed values
  auth.py              sign in and out, login_required, role_required
  security.py          CSRF token and security headers
  main.py              home, dashboard, privacy, error pages
  tickets.py           raise, queue, detail, assign, escalate, updates
  customer.py          the customer's requests and comments
  jobs.py              scheduling, week view, my schedule, job briefs
  articles.py          the knowledge base
  reports.py           KPIs for managers
  settings.py          accessibility settings
  filters.py           how dates are shown
  templates/           Jinja templates, one folder per feature
  static/css/style.css all the styles
  static/js/charts.js  bar charts drawn from the report tables
docs/
  test-log.md          fifty manual tests and their results
  change-log.md        what each step changed, and why
  sources.md           what came from where, and the use of AI
```

## Une courte démonstration, pour une vidéo

1. Connectez-vous en tant que client de Brightwell et créez une demande.
2. Connectez-vous en tant que Tier 1 : trouvez-la dans la file, lisez un article lié, puis
   escaladez-la vers le Tier 2 avec une raison.
3. Connectez-vous en tant que responsable : assignez-la à Sam Okafor et planifiez une visite.
4. Connectez-vous en tant que Tier 2 : ouvrez My schedule, lisez la fiche d'intervention et marquez-la comme terminée.
5. De retour en tant que client : le fil chronologique montre la visite, mais pas les notes
   internes.
6. En tant que responsable, ouvrez Reports. Puis activez le texte plus grand et le contraste élevé.

## À regarder

- `docs/test-log.md` : ce qui a été testé, ce qui a échoué et comment cela a été corrigé.
- `docs/sources.md` : de quelle documentation vient chaque technique, et ce qui
  a été changé après vérification du code écrit par l'IA.
- Lancez `git log --oneline` et `git checkout step-07` (n'importe quelle étape) pour voir
  l'application telle qu'elle était à ce moment-là. `git checkout main` permet de revenir.

## Apprendre cette étape

Voici l'étape 16 sur 16 de **Task 2. Developing the solution**, une série gratuite de leçons de T Level Digital Software Development, en anglais, qui construit le centre d'assistance Netheret en sprints agiles avec Python et Flask. Lisez la leçon de cette étape :
[Journal des modifications, sources et application terminée](https://mitsurutech.co.uk/resources/t-level/dsd-t2-16-final).

- Étape précédente : [étape 15, tester à la main et le journal de tests](https://github.com/mitsurutech/netheret-helpdesk-15-test-log)
- [Toutes les leçons gratuites de T Level Digital](https://mitsurutech.co.uk/resources/t-level)
- [Enseigner ces leçons à votre classe sur MitsuruTech](https://mitsurutech.co.uk/fr/learning), [voir les tarifs](https://mitsurutech.co.uk/fr/pricing) ou
  [commencer une année gratuite pour votre établissement](https://mitsurutech.co.uk/fr/signup)

## À propos

Écrit par [Mitsuru Technologies](https://mitsurutech.co.uk/fr) (MitsuruTech) comme exemple pédagogique pour le T Level Digital
Software Development. Le cahier des charges Netheret IT Support Solutions provient du matériel d'évaluation type de Pearson ; ce code
et ses notes sont les nôtres, et ne sont ni publiés, ni soutenus, ni approuvés par Pearson ou le Department for Education.
« T Level » est une marque déposée du Department for Education.
