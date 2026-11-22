# Netheret-Helpdesk, Schritt 16: Endfassung

[English](README.md) | [Français](README.fr.md) | [Español](README.es.md) | [日本語](README.ja.md) | [Deutsch](README.de.md)

Ein Beispiel für den Unterricht. In sechzehn Schritten haben wir eine Helpdesk-Webanwendung für Netheret gebaut, ein erfundenes Unternehmen, das die IT kleiner Firmen betreut. Dies ist die fertige Anwendung, mit ihrem Änderungsprotokoll, ihren Quellen und ihrem Testprotokoll.

## Was die Anwendung kann

| Rolle | Was sie tun kann |
|------|------------------|
| Kunde | Supportanfragen stellen, die Anfragen der eigenen Firma im Verlauf verfolgen, Kommentare hinzufügen, die Wissensdatenbank lesen |
| Tier-1-Agent | Die Warteschlange sichten, Anfragen zuweisen und eskalieren, interne oder für den Kunden sichtbare Einträge hinzufügen, Anfragen für Kunden erfassen, die Wissensdatenbank nutzen und schreiben |
| Techniker in Tier 2 / Tier 3 | Eskalierte Anfragen übernehmen und bearbeiten, den eigenen Plan sehen, Einsatzaufträge lesen und den Fortschritt festhalten |
| Manager | Alles, was das Personal kann, dazu an jede Person zuweisen, Vor-Ort-Einsätze planen und die Berichte sehen |

Alle können unter Settings größeren Text und hohen Kontrast wählen.

## Starten

Sie brauchen Python 3.10 oder neuer.

```
python -m venv .venv
source .venv/bin/activate        # on Windows: .venv\Scripts\activate
pip install -r requirements.txt
python seed.py
flask --app helpdesk run --debug
```

Öffnen Sie http://127.0.0.1:5000. `python seed.py` löscht alles und lädt
bei jedem Aufruf frische Beispieldaten.

### Demo-Konten

Alle verwenden das Demo-Passwort `password123`, das nur für diese Beispieldaten
gedacht ist.

| Rolle | E-Mail |
|------|-------|
| Manager | `manager@netheret.example` |
| Tier 1 | `tier1@netheret.example` |
| Tier 2 | `tier2@netheret.example` |
| Tier 3 | `tier3@netheret.example` |
| Kunde (Brightwell Bakery) | `customer@brightwell.example` |
| Kunde (Harbour Dental Practice) | `customer@harbour.example` |

### Auf einem echten Server

Setzen Sie `SECRET_KEY` auf einen langen Zufallswert und hinter HTTPS `SESSION_COOKIE_SECURE=1`,
und betreiben Sie die Anwendung mit einem Webserver für den Produktivbetrieb statt mit
`flask run`. Ohne `SECRET_KEY` erzeugt die Anwendung bei jedem Start einen zufälligen Schlüssel,
was auf Ihrem eigenen Computer in Ordnung ist.

## Wie der Code aufgebaut ist

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

## Eine kurze Demo, für eine Bildschirmaufnahme

1. Melden Sie sich als Kunde von Brightwell an und stellen Sie eine Anfrage.
2. Melden Sie sich als Tier 1 an: Finden Sie die Anfrage in der Warteschlange, lesen Sie einen passenden Artikel und
   eskalieren Sie sie dann mit Begründung an Tier 2.
3. Melden Sie sich als Manager an: Weisen Sie sie Sam Okafor zu und planen Sie einen Besuch.
4. Melden Sie sich als Tier 2 an: Öffnen Sie My schedule, lesen Sie den Einsatzauftrag und markieren Sie ihn als erledigt.
5. Zurück als Kunde: Der Verlauf zeigt den Besuch, aber nicht die internen
   Notizen.
6. Öffnen Sie als Manager Reports. Schalten Sie dann größeren Text und hohen Kontrast ein.

## Worauf Sie achten sollten

- `docs/test-log.md`: was getestet wurde, was fehlschlug und wie es behoben wurde.
- `docs/sources.md`: aus welcher Dokumentation jedes Muster stammt und was
  nach der Prüfung des von der KI geschriebenen Codes geändert wurde.
- Führen Sie `git log --oneline` und `git checkout step-07` (beliebiger Schritt) aus, um
  die Anwendung so zu sehen, wie sie an diesem Punkt war. `git checkout main` bringt Sie zurück.

## Diesen Schritt lernen

Dies ist Schritt 16 von 16 aus **Task 2. Developing the solution**, einer kostenlosen Reihe von Lektionen zu T Level Digital Software Development auf Englisch, die den Helpdesk von Netheret in agilen Sprints mit Python und Flask baut. Lesen Sie die Lektion zu diesem Schritt:
[Änderungsprotokoll, Quellen und die fertige Anwendung](https://mitsurutech.co.uk/resources/t-level/dsd-t2-16-final).

- Vorheriger Schritt: [Schritt 15, Testen von Hand und das Testprotokoll](https://github.com/mitsurutech/netheret-helpdesk-15-test-log)
- [Alle kostenlosen Lektionen zu T Level Digital](https://mitsurutech.co.uk/resources/t-level)
- [Diese Lektionen mit Ihrer Klasse auf MitsuruTech unterrichten](https://mitsurutech.co.uk/de/learning), [die Preise ansehen](https://mitsurutech.co.uk/de/pricing) oder
  [ein kostenloses Jahr für Ihre Schule beginnen](https://mitsurutech.co.uk/de/signup)

## Über dieses Beispiel

Geschrieben von [Mitsuru Technologies](https://mitsurutech.co.uk/de) (MitsuruTech) als Unterrichtsbeispiel für T Level Digital
Software Development. Die Aufgabenstellung Netheret IT Support Solutions stammt aus dem Muster-Prüfungsmaterial von Pearson; dieser Code
und seine Erläuterungen sind unsere eigenen und werden weder von Pearson noch vom Department for Education veröffentlicht, unterstützt oder genehmigt.
„T Level“ ist eine eingetragene Marke des Department for Education.
