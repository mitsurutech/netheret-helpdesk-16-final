"""General pages that do not belong to one feature."""
from flask import Blueprint, g, redirect, render_template, url_for

from .auth import login_required
from .extensions import db
from .models import Ticket

bp = Blueprint("main", __name__)

# How each role is shown to people.
ROLE_NAMES = {
    "customer": "a customer",
    "tier1": "a Tier 1 agent",
    "tier2": "a Tier 2 engineer",
    "tier3": "a Tier 3 engineer",
    "manager": "a manager",
}


# Friendly pages for errors, in plain words, with a way back.
@bp.app_errorhandler(400)
def bad_request(error):
    return render_template(
        "errors/error.html", heading="That did not work",
        message="The form was out of date or did not come from this site. "
                "Go back, reload the page and try again.",
    ), 400


@bp.app_errorhandler(403)
def forbidden(error):
    return render_template(
        "errors/error.html", heading="You cannot open this page",
        message="Your account does not have access to this page.",
    ), 403


@bp.app_errorhandler(405)
def wrong_method(error):
    # Test log T09: typing /signout into the address bar showed Flask's own
    # "Method Not Allowed" page.
    return render_template(
        "errors/error.html", heading="Use the button on the page",
        message="This address only works from a button on the site, such as Sign out.",
    ), 405


@bp.app_errorhandler(404)
def not_found(error):
    return render_template(
        "errors/error.html", heading="Page not found",
        message="Check the address, or go back and follow a link.",
    ), 404


@bp.route("/")
def home():
    if g.user:
        return redirect(url_for("main.dashboard"))
    return render_template("home.html")


@bp.route("/privacy")
def privacy():
    return render_template("privacy.html")


@bp.route("/dashboard")
@login_required
def dashboard():
    open_tickets = []
    if g.user.role == "customer":
        open_tickets = db.session.scalars(
            db.select(Ticket)
            .where(Ticket.company_id == g.user.company_id,
                   Ticket.status.in_(["new", "open", "waiting"]))
            .order_by(Ticket.created_at.desc())
        ).all()
    return render_template("dashboard.html", role_names=ROLE_NAMES, open_tickets=open_tickets)
