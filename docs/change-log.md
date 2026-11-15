# Change log

One entry for each step of the build. Each step is a commit tagged
`step-01` to `step-16`, so you can check out any one of them and run it.

## Step 01: setup
**What changed:** a Flask app made by `create_app()`, one page in a
blueprint, `requirements.txt` with pinned versions, and `.gitignore`.
**Why:** to prove the tools work before writing any features, and so that
everybody installs exactly the same library versions.

## Step 02: layout
**What changed:** a Jinja base template with header, menu, main and footer,
a home page that extends it, and a stylesheet with colour variables, a skip
link and a visible focus ring.
**Why:** every later page gets the same layout and the same accessible
structure without repeating it.

## Step 03: database
**What changed:** the six tables from the ERD as models (`Company`, `User`,
`Ticket`, `TicketUpdate`, `Job`, `Article`), the lists of allowed values,
password hashing on `User`, and `seed.py` with sample data.
**Why:** every feature needs data, and sample data lets us see pages working
before the forms to make that data exist.

## Step 04: sign-in
**What changed:** sign in and sign out, the user id kept in the session,
`login_required` and `role_required` written by hand, a secret key from the
environment, and a dashboard for each role.
**Why:** almost everything after this depends on knowing who is signed in
and what their role allows.

## Step 05: raise a request
**What changed:** the raise a request form for customers (and for Tier 1
and managers taking a phone call), server-side checks with an error summary
and messages beside each field, and a confirmation page with the reference.
**Why:** logging a support request is the first thing the brief asks for.

## Step 06: queue
**What changed:** the request queue for staff with filters for status,
priority, tier and who it is assigned to, sorted by urgency, and the request
detail page.
**Why:** Tier 1 needs to see and triage what has come in.

## Step 07: timeline
**What changed:** assign, take, escalate with a reason, change status and
add updates (internal or customer-visible), all recorded on a timeline;
`resolved_at` kept in step with the status.
**Why:** the brief asks to track a request's progress and keep people
informed, and the timeline is the record of who did what.

## Step 08: jobs
**What changed:** managers schedule on-site jobs with a double booking
check, a week view of jobs, and a link from a request to schedule a visit,
which tells the customer.
**Why:** Netheret plans and schedules on-site work.

## Step 09: my schedule
**What changed:** an engineer's own schedule, the job brief page, and
progress (in progress, done, notes) with a note on the request's timeline
when a job is done.
**Why:** Tier 2 and Tier 3 asked for personal schedules and job briefs.

## Step 10: knowledge base
**What changed:** search by words and category, read, write and edit
(staff), "did this help?", and related articles on a request's page.
**Why:** Tier 1 asked for a knowledge base so they can fix more requests
without escalating.

## Step 11: customer view
**What changed:** customers see their company's requests, follow a
timeline that hides internal notes, and add comments that reopen a request
that was waiting or resolved.
**Why:** customers should be kept informed, and must only see their own
company's data.

## Step 12: reports
**What changed:** a reports page for managers with KPIs from SQL queries
(open by priority, time to resolve, requests per person, first-contact
resolution, old open requests, jobs done, helpful articles) and bar charts
drawn from the tables with plain JavaScript.
**Why:** the brief asks for data about how systems and teams are
performing.

## Step 13: accessibility
**What changed:** larger text and high contrast saved on each user's row
and applied as CSS classes, messages announced to screen readers, and
plain-words error pages.
**Why:** staff asked for accessibility features, and the Equality Act 2010
expects reasonable adjustments.

## Step 14: security and law
**What changed:** a CSRF token written by hand on every POST form, security
headers, safer session cookie settings, and a privacy notice.
**Why:** to protect accounts and data, and to meet UK GDPR's duty to tell
people how their data is used.

## Step 15: test log
**What changed:** fifty manual tests recorded in `docs/test-log.md`, and
fixes for the six that failed: a friendly 405 page, no escalating of
resolved requests, a server-side length check on job titles, a clearer
double booking message, telling the customer when a visit is cancelled, and
counting article views once per person.
**Why:** to show the app meets its acceptance criteria, and to find what
reading the code had missed.

## Step 16: final
**What changed:** this change log, `docs/sources.md`, a full README, and
small tidying (the engineer dashboard works out its tier in a clearer way).
**Why:** so somebody else can understand, run, check and carry on with the
project.
