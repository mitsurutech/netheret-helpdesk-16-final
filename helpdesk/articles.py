"""The knowledge base: articles about known problems and how to fix them."""
from flask import Blueprint, flash, g, redirect, render_template, request, session, url_for

from .auth import login_required, role_required
from .extensions import db
from .models import CATEGORIES, STAFF_ROLES, Article

bp = Blueprint("kb", __name__)


@bp.route("/kb")
@login_required
def search():
    q = request.args.get("q", "").strip()
    category = request.args.get("category", "")

    query = db.select(Article)
    if q:
        # icontains means "contains, ignoring capitals". autoescape=True makes
        # % and _ in the search count as ordinary letters, not wildcards.
        query = query.where(
            Article.title.icontains(q, autoescape=True)
            | Article.symptoms.icontains(q, autoescape=True)
            | Article.solution.icontains(q, autoescape=True)
        )
    if category in CATEGORIES:
        query = query.where(Article.category == category)
    # The articles people found most helpful come first.
    articles = db.session.scalars(query.order_by(Article.helpful_count.desc(), Article.title)).all()
    return render_template("kb/search.html", articles=articles, q=q, category=category,
                           categories=CATEGORIES)


@bp.route("/kb/<int:article_id>")
@login_required
def read(article_id):
    article = db.get_or_404(Article, article_id)
    # Count each person once per session. Test log T41: reloading the page,
    # or pressing "Yes, this helped", added another view every time.
    viewed = session.get("viewed_articles", [])
    if article.id not in viewed:
        article.views += 1
        db.session.commit()
        session["viewed_articles"] = viewed + [article.id]
    already_voted = article.id in session.get("helpful_votes", [])
    return render_template("kb/read.html", article=article, already_voted=already_voted)


@bp.route("/kb/<int:article_id>/helpful", methods=["POST"])
@login_required
def helpful(article_id):
    """The "Did this help?" button. Each person counts once per session."""
    article = db.get_or_404(Article, article_id)
    votes = session.get("helpful_votes", [])
    if article.id not in votes:
        article.helpful_count += 1
        db.session.commit()
        # Save the list back into the session so Flask stores the change.
        session["helpful_votes"] = votes + [article.id]
    flash("Thank you. Your feedback helps us improve the knowledge base.")
    return redirect(url_for("kb.read", article_id=article.id))


def check_article_form(form):
    errors = {}
    title = form.get("title", "").strip()
    if not title:
        errors["title"] = "Enter a title."
    elif len(title) > 150:
        errors["title"] = "The title must be 150 characters or fewer."
    if form.get("category") not in CATEGORIES:
        errors["category"] = "Choose a category."
    if not form.get("symptoms", "").strip():
        errors["symptoms"] = "Describe the symptoms: what the user sees."
    if not form.get("solution", "").strip():
        errors["solution"] = "Write the solution, step by step."
    return errors


@bp.route("/kb/new", methods=["GET", "POST"])
@bp.route("/kb/<int:article_id>/edit", methods=["GET", "POST"])
@role_required(*STAFF_ROLES)
def edit(article_id=None):
    """One page for writing a new article and editing an old one."""
    article = db.get_or_404(Article, article_id) if article_id else None
    errors = {}
    if request.method == "POST":
        form = request.form
        errors = check_article_form(form)
        if not errors:
            if article is None:
                article = Article(author=g.user)
                db.session.add(article)
            article.title = form["title"].strip()
            article.category = form["category"]
            article.symptoms = form["symptoms"].strip()
            article.solution = form["solution"].strip()
            db.session.commit()
            flash("Article saved.")
            return redirect(url_for("kb.read", article_id=article.id))
    elif article:
        # Editing: start with what the article says now.
        form = {"title": article.title, "category": article.category,
                "symptoms": article.symptoms, "solution": article.solution}
    else:
        form = {}
    return render_template("kb/edit.html", article=article, form=form, errors=errors,
                           categories=CATEGORIES)
