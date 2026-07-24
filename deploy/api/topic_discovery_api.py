from flask import Blueprint, jsonify, render_template, request

from deploy.routes.topic_discovery import topic_discovery

topic_discovery_bp = Blueprint(
    "topic_discovery",
    __name__,
    url_prefix="/topic_discovery",
)

@topic_discovery_bp.route("/")
def index():
    return render_template(
        "topic_discovery.html",
        active_page="topic_discovery",
    )

@topic_discovery_bp.route("/api/topic_discovery", methods=["GET"])
def topic_discovery_api():

    topic_id = request.args.get("topic_id", default=None, type=int)
    keyword = request.args.get("keyword", default=None, type=str)

    data = topic_discovery(topic_id=topic_id, keyword=keyword)

    return jsonify(data)