from flask import Blueprint, jsonify, render_template, request

from deploy.routes.collaboration.collaboration import (
    get_collaboration_graph,
    load_collaboration_data,
)

collaboration_bp = Blueprint(
    "collaboration",
    __name__,
    url_prefix="/collaboration",
)

@collaboration_bp.route("/")
def index():
    return render_template(
        "collaboration.html",
        active_page="collaboration",
    )

@collaboration_bp.route("/api/collaboration/years", methods=["GET"])
def collaboration_years_api():

    data = load_collaboration_data()
    papers_df = data["papers"]

    years = sorted(
        papers_df["publication_year"].dropna().unique().tolist()
    )

    return jsonify({"years": years})

@collaboration_bp.route("/api/collaboration/topics", methods=["GET"])
def collaboration_topics_api():

    data = load_collaboration_data()
    topics_df = data["topics"]

    topics = topics_df[["topic_id", "topic_name"]].to_dict("records")

    return jsonify({"topics": topics})

@collaboration_bp.route("/api/collaboration/graph", methods=["GET"])
def collaboration_graph_api():

    year = request.args.get("year", type=int)
    topic_id = request.args.get("topic_id", type=int)

    data = get_collaboration_graph(year=year, topic_id=topic_id)

    return jsonify(data)