# Netheret help desk, step 15: test log

A teaching example. Over sixteen steps we build a help desk web app for
Netheret, a made-up company that supports the IT of small businesses. This
step tests the whole app by hand, writes the results in a test log, and
fixes what the testing found.

## What this step adds

- `docs/test-log.md`: fifty tests, each with the requirement it checks, the
  steps, what we expected, what actually happened, pass or fail, and the fix.
- Six fixes, each with a comment in the code naming its test:
  - T09: a friendly page when an address is used the wrong way (`main.py`);
  - T21: resolved and closed requests can no longer be escalated
    (`tickets.py`, `detail.html`);
  - T30: the server checks the length of a job title (`jobs.py`);
  - T32: the double booking message names the days (`jobs.py`);
  - T36: cancelling a visit tells the customer (`jobs.py`);
  - T41: article views count each person once per session (`articles.py`).

## Run it

```
python -m venv .venv
source .venv/bin/activate        # on Windows: .venv\Scripts\activate
pip install -r requirements.txt
python seed.py
flask --app helpdesk run --debug
```

Run `python seed.py` before testing, so your numbers match the test log.
Every demo account uses the demo password `password123`.

## What to look at

- The "Actual" column says what really happened, even when it was wrong.
  A test log full of passes that nobody ran is worth nothing.
- Many failures were found by sending something the page never offers. The
  browser is not in charge of what the server receives.
- Try a test of your own from the list at the end of the log.

<!-- links -->
