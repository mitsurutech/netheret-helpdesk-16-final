"""On-site jobs: scheduling them and the week view."""
from datetime import date, datetime, timedelta

from flask import Blueprint, abort, flash, g, redirect, render_template, request, url_for

from .auth import role_required
from .extensions import db
from .models import ENGINEER_ROLES, JOB_KINDS, JOB_STATUSES, STAFF_ROLES, Company, Job, Ticket, User
from .tickets import add_update

bp = Blueprint("jobs", __name__)


def monday_of(day):
    """The Monday of the week that day is in (weekday() is 0 on Monday)."""
    return day - timedelta(days=day.weekday())


def find_clash(engineer_id, start, end):
    """Return a job that overlaps start to end for this engineer, or None.

    Two jobs overlap when each one starts before the other one ends.
    """
    jobs = db.session.scalars(
        db.select(Job).where(Job.engineer_id == engineer_id, Job.status != "cancelled")
    ).all()
    for job in jobs:
        if job.scheduled_start < end and start < job.scheduled_end:
            return job
    return None


@bp.route("/jobs")
@role_required(*STAFF_ROLES)
def week():
    """A calendar-style list of one week's jobs, Monday to Sunday."""
    try:
        chosen = date.fromisoformat(request.args.get("week", ""))
    except ValueError:
        chosen = date.today()
    monday = monday_of(chosen)
    start = datetime.combine(monday, datetime.min.time())
    end = start + timedelta(days=7)

    jobs = db.session.scalars(
        db.select(Job)
        .where(Job.scheduled_start >= start, Job.scheduled_start < end)
        .order_by(Job.scheduled_start)
    ).all()

    # Put the jobs into seven lists, one for each day of the week.
    days = []
    for number in range(7):
        day = monday + timedelta(days=number)
        days.append({
            "date": day,
            "jobs": [job for job in jobs if job.scheduled_start.date() == day],
        })
    return render_template(
        "jobs/week.html", days=days, monday=monday, today=date.today(),
        previous_week=monday - timedelta(days=7), next_week=monday + timedelta(days=7),
    )


def check_job_form(form):
    """Check the job form. Returns (errors, cleaned values).

    The checks go in the same order as the form, so the error summary does too.
    """
    errors = {}
    values = {}

    company = db.session.get(Company, int(form["company_id"])) if form.get("company_id", "").isdigit() else None
    if company is None:
        errors["company_id"] = "Choose the company the job is for."
    values["company"] = company

    # The request is optional, but if one is chosen it must be this company's.
    ticket = None
    if form.get("ticket_id"):
        ticket = db.session.get(Ticket, int(form["ticket_id"])) if form["ticket_id"].isdigit() else None
        if ticket is None or (company and ticket.company_id != company.id):
            errors["ticket_id"] = "Choose a request from the same company, or none."
    values["ticket"] = ticket

    engineer = db.session.get(User, int(form["engineer_id"])) if form.get("engineer_id", "").isdigit() else None
    if engineer is None or engineer.role not in ENGINEER_ROLES:
        errors["engineer_id"] = "Choose a Tier 2 or Tier 3 engineer."
    values["engineer"] = engineer

    values["title"] = form.get("title", "").strip()
    if not values["title"]:
        errors["title"] = "Enter a title for the job."
    elif len(values["title"]) > 150:
        # Test log T30: only the browser's maxlength stopped long titles.
        errors["title"] = "The title must be 150 characters or fewer."
    values["kind"] = form.get("kind")
    if values["kind"] not in JOB_KINDS:
        errors["kind"] = "Choose the kind of job."

    try:
        # A datetime-local box sends a value like 2026-11-17T09:30
        values["start"] = datetime.strptime(form.get("scheduled_start", ""), "%Y-%m-%dT%H:%M")
        if values["start"] < datetime.now():
            errors["scheduled_start"] = "The start must be in the future."
    except ValueError:
        values["start"] = None
        errors["scheduled_start"] = "Enter the date and time the job starts."

    duration = form.get("duration_minutes", "")
    if not duration.isdigit() or not 15 <= int(duration) <= 480:
        errors["duration_minutes"] = "Enter how long the job takes, from 15 to 480 minutes."
        values["duration"] = None
    else:
        values["duration"] = int(duration)

    values["brief"] = form.get("brief", "").strip()
    if not values["brief"]:
        errors["brief"] = "Write the brief: what the engineer needs to do and know."

    # Only look for a clash once everything it needs is valid.
    if engineer and values["start"] and values["duration"] and not errors:
        end = values["start"] + timedelta(minutes=values["duration"])
        clash = find_clash(engineer.id, values["start"], end)
        if clash:
            # Test log T32: the dates are shown because a job can run past
            # midnight, and "that day" was then wrong.
            errors["scheduled_start"] = (
                f"{engineer.name} already has \"{clash.title}\" from "
                f"{clash.scheduled_start:%a %d %b %H:%M} to {clash.scheduled_end:%a %d %b %H:%M}."
            )
    return errors, values


@bp.route("/jobs/new", methods=["GET", "POST"])
@role_required("manager")
def new_job():
    errors = {}
    form = request.form
    if request.method == "POST":
        errors, values = check_job_form(form)
        if not errors:
            job = Job(
                company=values["company"], ticket=values["ticket"],
                engineer=values["engineer"], title=values["title"],
                brief=values["brief"], kind=values["kind"],
                scheduled_start=values["start"], duration_minutes=values["duration"],
                status="scheduled",
            )
            db.session.add(job)
            if job.ticket:
                # Tell the customer on their request's timeline.
                add_update(job.ticket, f"An engineer will visit on {job.scheduled_start:%A %d %B at %H:%M}.", True)
            db.session.commit()
            flash(f"Job scheduled for {job.engineer.name}.")
            return redirect(url_for("jobs.week", week=job.scheduled_start.date().isoformat()))
    else:
        # The detail page links here with ?ticket_id=..., so fill in what we can.
        form = {}
        ticket = db.session.get(Ticket, int(request.args["ticket_id"])) if request.args.get("ticket_id", "").isdigit() else None
        if ticket:
            form = {"ticket_id": str(ticket.id), "company_id": str(ticket.company_id), "title": ticket.title}

    companies = db.session.scalars(db.select(Company).order_by(Company.name)).all()
    engineers = db.session.scalars(
        db.select(User).where(User.role.in_(ENGINEER_ROLES)).order_by(User.name)
    ).all()
    tickets = db.session.scalars(
        db.select(Ticket).where(Ticket.status.in_(["new", "open", "waiting"])).order_by(Ticket.id)
    ).all()
    return render_template(
        "jobs/new.html", form=form, errors=errors, companies=companies,
        engineers=engineers, tickets=tickets, kinds=JOB_KINDS,
    )


@bp.route("/jobs/mine")
@role_required(*ENGINEER_ROLES)
def my_schedule():
    """An engineer's own jobs from today onwards, grouped by day."""
    start_of_today = datetime.combine(date.today(), datetime.min.time())
    jobs = db.session.scalars(
        db.select(Job)
        .where(Job.engineer_id == g.user.id, Job.status != "cancelled")
        # Also show older jobs that were started but never marked done.
        .where((Job.scheduled_start >= start_of_today) | (Job.status == "in_progress"))
        .order_by(Job.scheduled_start)
    ).all()

    # Group the jobs by day: {date: [jobs on that date]}. Dictionaries keep
    # the order things were added, and the jobs are already in time order.
    days = {}
    for job in jobs:
        days.setdefault(job.scheduled_start.date(), []).append(job)
    return render_template("jobs/mine.html", days=days, today=date.today())


@bp.route("/jobs/<int:job_id>")
@role_required(*STAFF_ROLES)
def brief(job_id):
    """The job brief: everything an engineer needs on site."""
    job = db.get_or_404(Job, job_id)
    if not job.can_be_seen_by(g.user):
        abort(403)
    # Engineers can move a job along; only a manager can cancel one.
    statuses = JOB_STATUSES if g.user.role == "manager" else ["scheduled", "in_progress", "done"]
    return render_template("jobs/brief.html", job=job, statuses=statuses)


@bp.route("/jobs/<int:job_id>/progress", methods=["POST"])
@role_required(*STAFF_ROLES)
def progress(job_id):
    """Mark progress on a job: its status and the engineer's notes."""
    job = db.get_or_404(Job, job_id)
    if not job.can_be_updated_by(g.user):
        abort(403)
    new_status = request.form.get("status", "")
    allowed = JOB_STATUSES if g.user.role == "manager" else ["scheduled", "in_progress", "done"]
    if new_status not in allowed:
        flash("Choose a status from the list.")
        return redirect(url_for("jobs.brief", job_id=job.id))

    finished_now = new_status == "done" and job.status != "done"
    cancelled_now = new_status == "cancelled" and job.status != "cancelled"
    job.status = new_status
    job.notes = request.form.get("notes", "").strip()
    if finished_now and job.ticket:
        # Record the visit on the request's timeline for the help desk.
        add_update(job.ticket, f"On-site job \"{job.title}\" done. Notes: {job.notes or 'none'}", False)
    if cancelled_now and job.ticket:
        # Test log T36: the customer was told about the visit but not that it
        # was cancelled.
        add_update(job.ticket, f"The visit on {job.scheduled_start:%A %d %B at %H:%M} is cancelled. "
                               "We will contact you to arrange another time.", True)
    db.session.commit()
    flash("Job updated.")
    return redirect(url_for("jobs.brief", job_id=job.id))
