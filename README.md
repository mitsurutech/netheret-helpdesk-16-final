# Netheret help desk, step 16: final

A teaching example. Over sixteen steps we built a help desk web app for
Netheret, a made-up company that supports the IT of small businesses. This
is the finished app, with its change log, sources and test log.

## What the app does

| Role | What they can do |
|------|------------------|
| Customer | Raise support requests, follow their company's requests on a timeline, add comments, read the knowledge base |
| Tier 1 agent | Triage the queue, assign and escalate requests, add internal or customer-visible updates, log requests for customers, use and write the knowledge base |
| Tier 2 / Tier 3 engineer | Take and work escalated requests, see their own schedule, read job briefs and mark progress |
| Manager | Everything staff can do, plus assign to anybody, schedule on-site jobs and see the reports |

Everybody can choose larger text and high contrast in Settings.

## Run it

You need Python 3.10 or newer.

```
python -m venv .venv
source .venv/bin/activate        # on Windows: .venv\Scripts\activate
pip install -r requirements.txt
python seed.py
flask --app helpdesk run --debug
```

Open http://127.0.0.1:5000. `python seed.py` deletes everything and loads
fresh sample data whenever you run it.

### Demo accounts

All of them use the demo password `password123`, which is for this sample
data only.

| Role | Email |
|------|-------|
| Manager | `manager@netheret.example` |
| Tier 1 | `tier1@netheret.example` |
| Tier 2 | `tier2@netheret.example` |
| Tier 3 | `tier3@netheret.example` |
| Customer (Brightwell Bakery) | `customer@brightwell.example` |
| Customer (Harbour Dental Practice) | `customer@harbour.example` |

### On a real server

Set `SECRET_KEY` to a long random value and `SESSION_COOKIE_SECURE=1`
behind HTTPS, and run the app with a production web server rather than
`flask run`. Without `SECRET_KEY` the app makes a random key each time it
starts, which is fine on your own computer.

## How the code is laid out

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

## A short demo, for a screencast

1. Sign in as the Brightwell customer and raise a request.
2. Sign in as Tier 1: find it in the queue, read a related article, then
   escalate it to Tier 2 with a reason.
3. Sign in as the manager: assign it to Sam Okafor and schedule a visit.
4. Sign in as Tier 2: open My schedule, read the job brief and mark it done.
5. Back as the customer: the timeline shows the visit, but not the internal
   notes.
6. As the manager, open Reports. Then turn on larger text and high contrast.

## What to look at

- `docs/test-log.md`: what was tested, what failed and how it was fixed.
- `docs/sources.md`: which documentation each pattern came from, and what
  was changed after checking the AI-written code.
- Run `git log --oneline` and `git checkout step-07` (any step) to see the
  app as it was at that point. `git checkout main` comes back.

<!-- links -->
