# Manual test log

The app was tested by hand at the end of step 14, using the sample data from
`python seed.py` (so the numbers below match a fresh database). Forms were
sent with `curl` from the command line, including requests a normal browser
would never send (a missing CSRF token, a value that is not on a list, a
role sending a form it is not shown), and pages were looked at in Chrome,
including with large text and high contrast on.

Each test names the epic from the product backlog it checks (E1 accounts and
access, E2 support requests, E3 on-site jobs, E4 knowledge base, E5
insights, E6 accessibility and quality) and the acceptance criterion.

Six tests failed. Each was fixed in step 15 and tested again; the fix is in
the last column, and the code has a comment naming the test.

| ID | Test | Requirement or acceptance criterion | Steps | Expected | Actual | Pass/fail | Fix |
|----|------|-------------------------------------|-------|----------|--------|-----------|-----|
| T01 | Sign in | E1: staff and customers sign in with email and password | Sign in as `manager@netheret.example` | Dashboard says "Hello, Maya Patel" | Dashboard says "Hello, Maya Patel. You are signed in as a manager." | Pass | |
| T02 | Wrong password | E1: a failed sign in gives a clear error that does not say which part was wrong | Sign in with the right email and a wrong password | Error message, email still filled in | "The email address or password is not right.", email kept | Pass | |
| T03 | Email in capitals | E1: sign in should not depend on capital letters in the email | Sign in as `Manager@netheret.example` | Signed in | Signed in | Pass | |
| T04 | Page needs sign in | E1: pages are only for signed-in users | Open `/dashboard` signed out | Sent to sign in with a message | Redirected to Sign in, "Please sign in to see that page." | Pass | |
| T05 | Customer cannot see the queue | E1: roles limit what each user can do | As a customer open `/queue` | Refused | "You cannot open this page" (403) | Pass | |
| T06 | Engineer cannot raise requests | E1: roles | As `tier2@` open `/requests/new` | Refused | 403 | Pass | |
| T07 | Sign out | E1: users can sign out | Press Sign out, then open `/dashboard` | Signed out, dashboard needs sign in again | "You have signed out.", dashboard redirects to Sign in | Pass | |
| T08 | Other company's request | E1: customers only see their own company's requests | As Brightwell's customer open `/my/requests/2` (Harbour's) | Not shown | 404 "Page not found"; posting a comment there also 404 | Pass | |
| T09 | Typing the sign out address | E6: clear errors | Type `/signout` in the address bar | A plain-words page | Flask's own "405 Method Not Allowed" page, in technical words | Fail | Friendly 405 page: "Use the button on the page". Retested: pass |
| T10 | Form without CSRF token | E6: CSRF token on every POST form | Send the sign in form with `curl` and no `csrf_token` | Refused | 400 "That did not work"; with a wrong token also 400; with the right token, signed in | Pass | |
| T11 | Customer raises a request | E2: a customer can raise a request and gets a reference | As Brightwell's customer, fill in every field and send | Reference shown, request is for Brightwell | "Your reference is NTH-0017", company Brightwell Bakery | Pass | |
| T12 | Empty request form | E2, E6: clear errors next to each field | Send the form empty | Every problem listed and linked to its field | Four messages in a summary, each a link, and each beside its field | Pass | |
| T13 | HTML in a title | E6: text is escaped | Title `<script>alert(1)</script>` | Shown as text | Shown as `&lt;script&gt;...`, nothing ran | Pass | |
| T14 | Tier 1 logs a phoned-in request | E2: staff can log a request for a customer | As `tier1@`, send without choosing a company, then with Harbour | Company required; then saved for Harbour | "Choose the customer's company."; then NTH-0018 for Harbour Dental Practice | Pass | |
| T15 | Queue order | E2: triage the most urgent first | Open Queue | Open requests only, critical first | 8 requests, NTH-0010 (critical) first | Pass | |
| T16 | Queue filters | E2: filter by status, priority, tier and assigned | Priority Critical, Any status | Only critical requests | 2 requests, both critical; "Nobody yet" gives 3, "Me" + Tier 1 gives 2 | Pass | |
| T17 | Nonsense filter values | E6: robust to bad input | `/queue?status=bogus&tier=9&assigned=abc` | Ignored, no error | Page loads with those filters ignored | Pass | |
| T18 | Assign a new request | E2: assign | Assign NTH-0013 to Tom Reid | Assigned, status open, on the timeline | "NTH-0013 is now assigned to Tom Reid", status Open, timeline "Assigned to Tom Reid." | Pass | |
| T19 | Escalate | E2: escalate tier, with a reason | Escalate NTH-0013 with no reason, then with one | Refused without a reason; then Tier 2 and unassigned | "Say why the request is being escalated..."; then Tier 2, "Nobody yet" | Pass | |
| T20 | Escalate down | E2: escalation only goes up | Send `tier=1` for a Tier 1 request with `curl` | Refused | "Choose a higher tier to escalate to." | Pass | |
| T21 | Escalate a resolved request | E2: escalate is for requests still being worked on | Open resolved NTH-0001 and escalate it | Not offered, and refused | Offered and done: Tier 2, still "Resolved", unassigned, so nobody would act on it | Fail | The form is replaced by a note, and the server refuses unless the request is new, open or waiting. Retested: pass, and escalating an open request still works |
| T22 | Engineer assigns to somebody else | E1, E2: only Tier 1 and managers assign to others | As `tier2@`, send another person's id to `/assign` with `curl` | Refused; taking it for themselves works | 403; "Take this request" assigns it to Sam Okafor | Pass | |
| T23 | Resolve and reopen | E2: update status; time to resolve is recorded | Add an update with status Resolved, then one with Open | Resolved time shown, then removed | "Resolved" date appears, and goes when reopened | Pass | |
| T24 | Internal notes | E2: customer-visible and internal updates | As Brightwell's customer open NTH-0009 | Only updates marked for the customer | "Booked a visit..." shown; "Escalated to Tier 2..." (internal) not shown | Pass | |
| T25 | Customer replies to a resolved request | E2: customers add comments | Comment "It broke again" on NTH-0001 | Comment saved, request reopened, staff see it | Status Open; on the staff timeline with "Customer can see this" | Pass | |
| T26 | Customer comments on a closed request | E2 | As Harbour's customer comment on closed NTH-0002 | Refused with advice | No form shown; posting gives "This request is closed. Please raise a new request." | Pass | |
| T27 | Schedule a job from a request | E3: schedule a job and assign an engineer | Manager: "Schedule a job" on NTH-0012 | Company and request filled in; job on the week; customer told | Filled in; job on the week view; customer timeline "An engineer will visit on..." | Pass | |
| T28 | Empty job form | E3, E6 | Send the job form empty | All problems, in form order | Seven messages, in the same order as the fields | Pass | |
| T29 | Request from another company | E3: data agrees | Brightwell with Moorside's NTH-0012 | Refused | "Choose a request from the same company, or none." | Pass | |
| T30 | Very long job title | E6: the server checks every field | Send a 300 character title with `curl` | Refused | Saved: only the browser's `maxlength` was stopping it | Fail | Server checks the title is 150 characters or fewer. Retested: pass |
| T31 | Double booking | E3: an engineer cannot be in two places | Book Sam 09:00 to 10:00, then 09:30, then 10:00 | Second refused, third allowed | "Sam Okafor already has "Router swap"..."; the 10:00 job was saved | Pass | |
| T32 | Clash across midnight | E3, E6: clear errors | Book Sam 23:00 for 2 hours, then 00:30 the next day | Clash, with the right times and days | Clash found, but it said "from 23:00 to 01:00 that day", which is wrong | Fail | The message gives both days: "from Sun 22 Nov 23:00 to Mon 23 Nov 01:00". Retested: pass |
| T33 | Job in the past | E3 | Start of 1 January 2020 | Refused | "The start must be in the future." | Pass | |
| T34 | My schedule | E3: engineers see their own schedule | As `tier2@` open My schedule | Own jobs from today on | Only Sam's jobs: "Annual PC health check" on Tue 17 Nov | Pass | |
| T35 | Another engineer's job brief | E1, E3 | As `tier2@` open Priya's job `/jobs/3` | Refused, and no link to it | 403; the week view links only Sam's own job | Pass | |
| T36 | Cancelling a visit | E2, E3: keep the customer informed | Manager cancels the job for NTH-0010; customer opens NTH-0010 | Customer is told | Nothing on the customer's timeline | Fail | Cancelling a job from a request adds a customer-visible update. Retested: pass |
| T37 | Mark a job done | E3: mark progress | As `tier2@`: In progress, then Done with notes; try Cancelled with `curl` | Done noted on the request once; cancel refused | Note "On-site job ... done" on NTH-0009; "Choose a status from the list." for Cancelled | Pass | |
| T38 | Search the knowledge base | E4: search | Search "PRINTER" | Matches whatever the capitals | 2 articles | Pass | |
| T39 | Search with % | E4, E6 | Search "100%" | No error, % is a normal letter | "0 articles matching 100%" | Pass | |
| T40 | Did this help? | E4: mark helpful | Press "Yes, this helped" twice | Counted once | 17 to 18, then stays 18; the button is replaced by a thank you | Pass | |
| T41 | Article views | E5: views mean people reading | Open an article, reload, press "Yes, this helped" | One view | 23, then 25, then 26: every reload and every vote added a view | Fail | Each person counts once per session. Retested: stays at 23. Pass |
| T42 | Write and edit articles | E4: staff write and edit | `tier1@` writes "Monitor flickers", then edits it; a customer opens `/kb/new` | Saved and edited; customer refused | Saved, edited title shown; customer 403 and no Edit link | Pass | |
| T43 | KPI numbers | E5: KPIs are correct | Work the numbers out by hand from `seed.py` and compare | Same numbers | First-contact resolution 5 of 8 finished = 62%; low priority average (50 + 0.5) / 2 = 25.2 hours; 5 open requests older than 2 working days. All match | Pass | |
| T44 | Charts | E5, E6: charts with the numbers also as a table | Open Reports as the manager; as `tier1@` | Bars match the tables; tier1 refused | Bars and labels match each table; tier1 gets 403 | Pass | |
| T45 | Skip link and focus | E6: keyboard use | Check the page source of each page: the first link, and what kind of element each control is | Skip link first; every control reachable by keyboard | Skip link is the first link on every page and points at `main`; every control is a normal link, button or form field, which the keyboard reaches and the yellow focus ring outlines. Not yet tried with a keyboard by a keyboard-only user (see the end of the log) | Pass | |
| T46 | Labels | E6: every field has a label | Check each field's `id` has a `label for` on 13 pages | None missing | 42 fields, none missing a label, no repeated ids | Pass | |
| T47 | Larger text and high contrast | E6: settings saved per user | As `tier3@` choose Larger and high contrast, sign out and in again; look at Jobs and Reports | Settings kept and applied | `<html class="text-larger high-contrast">` after signing in again; badges, charts and links readable | Pass | |
| T48 | Bad settings value | E6 | Send `text_size=huge` | Refused | "Choose one of the text sizes." | Pass | |
| T49 | Headers and cookie | E6: security | Look at the response headers | CSP, no framing, no sniffing; cookie HttpOnly and SameSite | All four headers; `HttpOnly; SameSite=Lax` | Pass | |
| T50 | Privacy notice | E6: UK GDPR privacy notice | Look for the link on every page | Linked from the footer | "Privacy notice" in every footer; page explains data, purpose, retention, cookies and rights | Pass | |

## What is left to test

- Screen reader use (for example NVDA or VoiceOver), and a whole session
  with the keyboard only, by people who work that way every day.
- A full walk-through on a phone.
- The app with many more requests than the sample data, to see whether the
  queue needs pages.
