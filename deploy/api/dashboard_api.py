from flask import Blueprint, jsonify, render_template

from deploy.routes.dashboard import dashboard

dashboard_bp = Blueprint(
    "dashboard",
    __name__,
)

@dashboard_bp.route("/")
def index():
    return render_template(
        "dashboard.html",
        active_page="dashboard",
    )

@dashboard_bp.route("/api/dashboard")
def dashboard_api():
    return jsonify(dashboard())