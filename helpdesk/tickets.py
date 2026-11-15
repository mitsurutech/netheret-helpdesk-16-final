"""Support requests (tickets): raising them, the queue, the detail page and
the actions staff take on a request (assign, escalate, update)."""
from datetime import datetime

from flask import Blueprint, abort, flash, g, redirect, render_template, request, url_for
from sqlalchemy import case

from .auth import login_required, role_required
from .extensions import db
from .models import (
    CATEGORIES, PRIORITIES, STAFF_ROLES, STATUSES, TIERS, Article, Company, Ticket, TicketUpdate,
    User,
)

# Only these roles may give a request to somebody else. Everybody else on
# the staff can only take a request for themselves.
ASSIGNING_ROLES = ["tier1", "manager"]

bp = Blueprint("tickets", __name__)


def check_request_form(form, needs_company):
    """Check what was typed into the request form.

    Returns a dictionary of {field name: error message}. An empty dictionary
    means there were no problems.
    """
    errors = {}
    title = form.get("title", "").strip()
    if not title:
        errors["title"] = "Enter a short title for the problem."
    elif len(title) > 150:
        errors["title"] = "The title must be 150 characters or fewer."
    if not form.get("description", "").strip():
        errors["description"] = "Describe the problem."
    # Choices must be on the allowed list, even though the form only offers
    # those: somebody could send any value without using our form.
    if form.get("category") not in CATEGORIES:
        errors["category"] = "Choose a category."
    if form.get("priority") not in PRIORITIES:
        errors["priority"] = "Choose a priority."
    if needs_company:
        company_id = form.get("company_id", "")
        if not company_id.isdigit() or db.session.get(Company, int(company_id)) is None:
            errors["company_id"] = "Choose the customer's company."
    return errors


@bp.route("/requests/new", methods=["GET", "POST"])
@role_required("customer", "tier1", "manager")
def new_request():
    # Customers raise requests for their own company. Staff taking a phone
    # call raise them for a customer, so they choose the company.
    is_customer = g.user.role == "customer"
    errors = {}
    form = request.form
    if request.method == "POST":
        errors = check_request_form(form, needs_company=not is_customer)
        if not errors:
            ticket = Ticket(
                title=form["title"].strip(),
                description=form["description"].strip(),
                category=form["category"],
                priority=form["priority"],
                status="new",
                tier=1,
                company_id=g.user.company_id if is_customer else int(form["company_id"]),
                raised_by=g.user,
            )
            db.session.add(ticket)
            db.session.flush()  # gives the ticket its id
            ticket.set_reference()
            db.session.commit()
            return redirect(url_for("tickets.raised", ticket_id=ticket.id))

    companies = [] if is_customer else db.session.scalars(db.select(Company).order_by(Company.name)).all()
    return render_template(
        "tickets/new.html", form=form, errors=errors, companies=companies,
        categories=CATEGORIES, priorities=PRIORITIES,
    )


@bp.route("/requests/<int:ticket_id>/raised")
@login_required
def raised(ticket_id):
    ticket = db.get_or_404(Ticket, ticket_id)
    # A customer may only see their own company's requests. We answer 404
    # (not found) so they cannot even tell that the request exists.
    if g.user.role == "customer" and ticket.company_id != g.user.company_id:
        abort(404)
    return render_template("tickets/raised.html", ticket=ticket)


@bp.route("/queue")
@role_required(*STAFF_ROLES)
def queue():
    """The list of requests, with filters chosen from the form at the top.

    The filters are in the address (a GET form), so a filtered queue can be
    bookmarked or shared.
    """
    status = request.args.get("status", "active")
    priority = request.args.get("priority", "")
    tier = request.args.get("tier", "")
    assigned = request.args.get("assigned", "")

    query = db.select(Ticket)
    # Each filter adds one more WHERE condition to the query.
    if status == "active":
        query = query.where(Ticket.status.in_(["new", "open", "waiting"]))
    elif status in STATUSES:
        query = query.where(Ticket.status == status)
    if priority in PRIORITIES:
        query = query.where(Ticket.priority == priority)
    if tier.isdigit() and int(tier) in TIERS:
        query = query.where(Ticket.tier == int(tier))
    if assigned == "me":
        query = query.where(Ticket.assigned_to_id == g.user.id)
    elif assigned == "none":
        query = query.where(Ticket.assigned_to_id.is_(None))
    elif assigned.isdigit():
        query = query.where(Ticket.assigned_to_id == int(assigned))

    # Most urgent first: CASE turns each priority into a number to sort by.
    urgency = case({"critical": 0, "high": 1, "medium": 2, "low": 3}, value=Ticket.priority)
    query = query.order_by(urgency, Ticket.created_at)
    tickets = db.session.scalars(query).all()

    staff = db.session.scalars(
        db.select(User).where(User.role.in_(STAFF_ROLES)).order_by(User.name)
    ).all()
    return render_template(
        "tickets/queue.html", tickets=tickets, staff=staff,
        statuses=STATUSES, priorities=PRIORITIES, tiers=TIERS,
        chosen={"status": status, "priority": priority, "tier": tier, "assigned": assigned},
    )


@bp.route("/requests/<int:ticket_id>")
@role_required(*STAFF_ROLES)
def detail(ticket_id):
    ticket = db.get_or_404(Ticket, ticket_id)
    staff = db.session.scalars(
        db.select(User).where(User.role.in_(STAFF_ROLES)).order_by(User.name)
    ).all()
    # Knowledge base articles in the same category, most helpful first, so
    # Tier 1 can try a known fix before escalating.
    articles = db.session.scalars(
        db.select(Article).where(Article.category == ticket.category)
        .order_by(Article.helpful_count.desc()).limit(3)
    ).all()
    return render_template(
        "tickets/detail.html", ticket=ticket, staff=staff, statuses=STATUSES, articles=articles,
        higher_tiers=[tier for tier in TIERS if tier > ticket.tier],
        can_assign=g.user.role in ASSIGNING_ROLES,
    )


def add_update(ticket, body, visible_to_customer, status_change=None):
    """Write one entry on the request's timeline.

    Every action calls this, so the timeline is a full history of the request.
    """
    db.session.add(TicketUpdate(
        ticket=ticket, author=g.user, body=body,
        visible_to_customer=visible_to_customer, status_change=status_change,
    ))
    # Adding an update counts as a change to the request.
    ticket.updated_at = datetime.now()


def change_status(ticket, new_status):
    """Set a new status, and keep resolved_at in step with it."""
    ticket.status = new_status
    if new_status in ["resolved", "closed"]:
        if ticket.resolved_at is None:
            ticket.resolved_at = datetime.now()
    else:
        # Reopened: it is not resolved any more.
        ticket.resolved_at = None


@bp.route("/requests/<int:ticket_id>/assign", methods=["POST"])
@role_required(*STAFF_ROLES)
def assign(ticket_id):
    ticket = db.get_or_404(Ticket, ticket_id)
    person_id = request.form.get("assigned_to_id", "")
    person = db.session.get(User, int(person_id)) if person_id.isdigit() else None
    if person is None or not person.is_staff:
        flash("Choose a member of staff to assign the request to.")
        return redirect(url_for("tickets.detail", ticket_id=ticket.id))
    # Engineers may take a request themselves but not hand it to others.
    if g.user.role not in ASSIGNING_ROLES and person.id != g.user.id:
        abort(403)

    ticket.assigned_to = person
    status_change = None
    if ticket.status == "new":
        # Somebody is now working on it, so it is no longer new.
        change_status(ticket, "open")
        status_change = "open"
    add_update(ticket, f"Assigned to {person.name}.", False, status_change)
    db.session.commit()
    flash(f"{ticket.reference} is now assigned to {person.name}.")
    return redirect(url_for("tickets.detail", ticket_id=ticket.id))


@bp.route("/requests/<int:ticket_id>/escalate", methods=["POST"])
@role_required(*STAFF_ROLES)
def escalate(ticket_id):
    ticket = db.get_or_404(Ticket, ticket_id)
    new_tier = request.form.get("tier", "")
    reason = request.form.get("reason", "").strip()
    # Test log T21: a resolved or closed request could be escalated, which left
    # it unassigned at a higher tier with nobody needing to act.
    if ticket.status not in ["new", "open", "waiting"]:
        flash("Only open requests can be escalated. Reopen it with an update first.")
    elif not new_tier.isdigit() or int(new_tier) not in TIERS or int(new_tier) <= ticket.tier:
        flash("Choose a higher tier to escalate to.")
    elif not reason:
        flash("Say why the request is being escalated, so the next tier knows.")
    else:
        old_tier = ticket.tier
        ticket.tier = int(new_tier)
        # Unassign it, so the next tier's engineers see it as waiting for them.
        ticket.assigned_to = None
        status_change = None
        if ticket.status in ["new", "waiting"]:
            change_status(ticket, "open")
            status_change = "open"
        add_update(ticket, f"Escalated from Tier {old_tier} to Tier {ticket.tier}: {reason}",
                   False, status_change)
        db.session.commit()
        flash(f"{ticket.reference} escalated to Tier {ticket.tier}.")
    return redirect(url_for("tickets.detail", ticket_id=ticket.id))


@bp.route("/requests/<int:ticket_id>/updates", methods=["POST"])
@role_required(*STAFF_ROLES)
def add_staff_update(ticket_id):
    """Add a note to the timeline, and change the status if asked."""
    ticket = db.get_or_404(Ticket, ticket_id)
    body = request.form.get("body", "").strip()
    new_status = request.form.get("status", ticket.status)
    # A checkbox is only sent when it is ticked.
    visible = request.form.get("visible_to_customer") == "yes"

    if new_status not in STATUSES:
        flash("Choose a status from the list.")
    elif not body:
        flash("Write the update before saving it.")
    else:
        status_change = None
        if new_status != ticket.status:
            change_status(ticket, new_status)
            status_change = new_status
        add_update(ticket, body, visible, status_change)
        db.session.commit()
        flash("Update added.")
    return redirect(url_for("tickets.detail", ticket_id=ticket.id))
