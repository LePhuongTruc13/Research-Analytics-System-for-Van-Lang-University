import os
from flask import Flask

from deploy.api.dashboard_api import dashboard_bp
from deploy.api.topic_discovery_api import topic_discovery_bp
from deploy.api.collaboration_api import collaboration_bp
from deploy.api.knowledge_graph_api import knowledge_graph_bp

# ==========================================================
# Absolute paths — không phụ thuộc cách chạy / thư mục hiện tại
# ==========================================================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

app = Flask(
    __name__,
    template_folder=os.path.join(BASE_DIR, "templates"),
    static_folder=os.path.join(BASE_DIR, "static"),
)

app.register_blueprint(dashboard_bp)
app.register_blueprint(topic_discovery_bp)
app.register_blueprint(collaboration_bp)
app.register_blueprint(knowledge_graph_bp)


if __name__ == "__main__":

    print("=" * 60)
    print("Research Analytics — All Pages")
    print("=" * 60)
    print()
    print("Dashboard:        http://localhost:5001/")
    print("Topic Discovery:  http://localhost:5001/topic_discovery/")
    print("Collaboration:    http://localhost:5001/collaboration/")
    print("Knowledge Graph:  http://localhost:5001/knowledge_graph/")
    print()

    app.run(
        host="0.0.0.0",
        port=5001,
        debug=True,
    )