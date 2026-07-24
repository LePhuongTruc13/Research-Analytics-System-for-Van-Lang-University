from flask import Blueprint, jsonify, render_template, request

from deploy.routes.knowledge_graph.knowledge_graph import load_knowledge_graph_data
from deploy.routes.knowledge_graph.filter_author import filter_authors
from deploy.routes.knowledge_graph.graph import build_author_graph
from deploy.routes.knowledge_graph.node_detail import (
    node_author,
    node_paper,
    node_topic,
    node_institution,
)

knowledge_graph_bp = Blueprint(
    "knowledge_graph",
    __name__,
    url_prefix="/knowledge_graph",
)

@knowledge_graph_bp.route("/")
def index():
    return render_template(
        "knowledge_graph.html",
        active_page="knowledge_graph",
    )

@knowledge_graph_bp.route("/api/knowledge_graph/authors", methods=["GET"])
def authors_api():

    data = load_knowledge_graph_data()
    authors = filter_authors(data["authors"])

    return jsonify(authors.to_dict("records"))

@knowledge_graph_bp.route("/api/knowledge_graph/graph", methods=["GET"])
def graph_api():

    author_id = request.args.get("author_id", type=str)

    if author_id is None:
        return jsonify({"nodes": [], "edges": []})

    data = load_knowledge_graph_data()

    graph = build_author_graph(
        knowledge_graph=data["knowledge_graph"],
        author_id=author_id,
        max_papers=5,
    )

    return jsonify(graph)

@knowledge_graph_bp.route("/api/knowledge_graph/node_detail", methods=["GET"])
def node_detail_api():

    node_id = request.args.get("node_id", type=str)
    node_type = request.args.get("node_type", type=str)

    data = load_knowledge_graph_data()

    try:

        if node_type == "Author":
            detail = node_author(
                author_id=node_id,
                papers_df=data["papers"],
                paper_author_df=data["paper_author"],
                authors_df=data["authors"],
            )

        elif node_type == "Paper":
            detail = node_paper(
                paper_id=node_id,
                papers_df=data["papers"],
                paper_author_df=data["paper_author"],
            )

        elif node_type == "Topic":
            detail = node_topic(
                topic_id=node_id,
                topics_df=data["topics"],
            )

        elif node_type == "Institution":
            detail = node_institution(
                institution_id=node_id,
                institutions_df=data["institution"],
                author_institution_df=data["author_institution"],
            )

        else:
            detail = {}

    except Exception as e:
        print(f"[node_detail_api] node_id={node_id!r} node_type={node_type!r} error={e}")
        return jsonify({"error": str(e)}), 500

    return jsonify(detail)