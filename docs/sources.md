# Sources

What this project was built from, and what came from where.

## Documentation the code follows

| What | Where it came from | How it was used |
|------|--------------------|-----------------|
| The app factory, blueprints, `g.user`, `@bp.before_app_request` and a hand-written `login_required` | The Flask tutorial (flask.palletsprojects.com, "Tutorial", the "Blueprints and Views" page) | The same pattern in `helpdesk/__init__.py` and `helpdesk/auth.py`, extended with `role_required` |
| Flashing messages, template filters, error handlers, `url_for('static', ...)` | The Flask documentation ("Message Flashing", "Templates", "Handling Application Errors") | `base.html`, `filters.py`, the error handlers in `main.py` |
| Models with `Mapped` and `mapped_column`, `db.session.scalars(db.select(...))`, `db.get_or_404` | The Flask-SQLAlchemy 3.1 documentation ("Quick Start", "Models and Tables", "Queries") | `models.py` and every query |
| `case`, `func.count`, `func.avg`, `group_by`, `icontains(..., autoescape=True)` | The SQLAlchemy 2 documentation ("ORM Querying Guide", "Column Elements and Expressions") | The queue sort in `tickets.py`, the KPIs in `reports.py`, the search in `articles.py` |
| `julianday()` for subtracting dates | The SQLite documentation ("Date And Time Functions") | Average time to resolve in `reports.py` |
| `generate_password_hash` and `check_password_hash` | The Werkzeug documentation ("Utilities", security helpers) | `User.set_password` and `User.check_password` |
| `secrets.token_hex` and `secrets.compare_digest` | The Python documentation (the `secrets` module) | The secret key fallback and the CSRF token |
| The synchroniser token pattern for CSRF | OWASP Cross-Site Request Forgery Prevention Cheat Sheet | `security.py` |
| Security headers | MDN Web Docs (Content-Security-Policy, X-Frame-Options, X-Content-Type-Options, Referrer-Policy) | `add_security_headers` in `security.py` |
| Drawing on a canvas, `devicePixelRatio` | MDN Web Docs (Canvas tutorial, `Window.devicePixelRatio`) | `static/js/charts.js` |
| Skip links, `aria-current`, `aria-describedby`, error summaries, focus styles, contrast | WCAG 2.2 and the GOV.UK Design System's guidance on error summaries and error messages | The templates and `style.css` |
| What a privacy notice should cover | The ICO's guidance on the right to be informed (UK GDPR) | `privacy.html` |
| Phone numbers in the sample data | Ofcom's numbers set aside for TV and radio drama | `seed.py`, so no real business is rung |

No code was copied from these pages; the patterns were written out for this
project. The help desk brief this app answers is described in our own words.

## Use of AI

This project was written with an AI coding assistant, as a worked example
for the lessons. The assistant generated the code, templates, styles and
documents step by step, from a plan we wrote (the roles, data model, pages,
KPIs and sprint steps). Nothing was accepted because it looked right: each
step was run and used by hand before it was saved, and the test log in step
15 records the full check.

What was changed after checking the AI's work:

- `seed.py` (step 03): saving each request's reference also stamped
  `updated_at` with the current time, because the column updates itself on
  every change. The fix sets `updated_at` after the reference.
- The job form's error summary (step 08) listed problems in a different
  order from the fields. The checks were reordered to match the form.
- High contrast (step 13): the "Open" status badge, today's column border
  and some job titles used the brand colour, which became black on black.
  Each got its own high contrast colour, checked in screenshots.
- The test log text (step 15): the first draft said the keyboard test was
  done by pressing Tab, when it was checked in the page source. The wording
  was corrected to say what was really done, and a keyboard-only session was
  added to "What is left to test".
- The six failed tests in `docs/test-log.md` (T09, T21, T30, T32, T36, T41),
  each fixed in step 15 with a comment in the code.
