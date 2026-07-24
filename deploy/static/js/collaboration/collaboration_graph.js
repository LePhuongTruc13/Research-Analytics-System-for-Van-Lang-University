class CollaborationGraph {

    // ========================================================
    // CONSTRUCTOR
    // ========================================================

    constructor() {

        // ----------------------------------------------------
        // SVG
        // ----------------------------------------------------

        this.svg = d3.select(
            "#network-graph"
        );

        this.viewport = document.querySelector(
            ".graph-viewport"
        );

        if (!this.viewport) {
            throw new Error(
                "Không tìm thấy .graph-viewport"
            );
        }

        // ----------------------------------------------------
        // SIZE
        // ----------------------------------------------------

        this.width = this.viewport.clientWidth;

        this.height = this.viewport.clientHeight;

        this.svg

            .attr("width", this.width)

            .attr("height", this.height);

        // ----------------------------------------------------
        // MAIN CONTAINER
        // ----------------------------------------------------

        this.container = this.svg

            .append("g")

            .attr(
                "class",
                "graph-container"
            );

        // ----------------------------------------------------
        // LAYERS
        // ----------------------------------------------------

        this.edgeLayer = this.container
            .append("g")
            .attr("class", "edge-layer");

        this.metricLineLayer = this.container
            .append("g")
            .attr("class", "metric-line-layer");

        this.nodeLayer = this.container
            .append("g")
            .attr("class", "node-layer");

        this.metricNodeLayer = this.container
            .append("g")
            .attr("class", "metric-node-layer");

        this.labelLayer = this.container
            .append("g")
            .attr("class", "label-layer");

        // ----------------------------------------------------
        // DATA
        // ----------------------------------------------------

        this.nodes = [];

        this.edges = [];

        // ----------------------------------------------------
        // D3 ZOOM
        // ----------------------------------------------------

        this.zoom = d3.zoom()

            .scaleExtent([0.2, 5])

            .on(

                "zoom",

                (event) => {

                    this.container.attr(

                        "transform",

                        event.transform

                    );

                }

            );

        this.svg.call(
            this.zoom
        );

        // ----------------------------------------------------
        // FORCE SIMULATION
        // ----------------------------------------------------

        this.simulation = d3.forceSimulation()

            .alphaDecay(0.05)

            .force("link", d3.forceLink()
                .id(d => d.id)
                .distance(180)          
            )

            .force("charge", d3.forceManyBody()
                .strength(-900)         
                .distanceMax(500)       
            )

            .force("center", d3.forceCenter(
                this.width / 2,
                this.height / 2
            ))

            .force("collision", d3.forceCollide()
                .radius(d => (d._radius ?? 6) + 25)  
            );

        // ----------------------------------------------------
        // INITIALIZE
        // ----------------------------------------------------

        this.initialize();

    }

    // ========================================================
    // INITIALIZE
    // ========================================================

    initialize() {

        this.initializeResize();

    }

    // ========================================================
    // WINDOW RESIZE
    // ========================================================

    initializeResize() {

        window.addEventListener(

            "resize",

            () => {

                this.width =

                    this.viewport.clientWidth;

                this.height =

                    this.viewport.clientHeight;

                this.svg

                    .attr(
                        "width",
                        this.width
                    )

                    .attr(
                        "height",
                        this.height
                    );

                this.simulation.force(

                    "center",

                    d3.forceCenter(

                        this.width / 2,

                        this.height / 2

                    )

                );

                this.simulation

                    .alpha(1)

                    .restart();

            }

        );

    }

    // ========================================================
    // LOAD GRAPH
    // ========================================================

    loadGraph(graphData) {

        this.nodes =

            graphData.nodes || [];

        this.edges =

            graphData.edges || [];

        this.render();

        this.highlightTopBridges(3);

    }

    // ========================================================
    // RENDER
    //
    // Sẽ được hoàn thiện ở Part 2
    // ========================================================

    // ========================================================
    // RENDER
    // ========================================================

    render() {
        this.edgeLayer.selectAll("*").remove();
        this.nodeLayer.selectAll("*").remove();
        this.labelLayer.selectAll("*").remove();

        this.renderEdges();
        this.renderNodes();
        this.renderLabels();
        this.startSimulation();
        this.renderMetricNodes();   
        this.enableInteraction(); // 
    }

    // ========================================================
    // RENDER EDGES
    // ========================================================

    renderEdges() {

        this.edgeSelection =

            this.edgeLayer

                .selectAll("line")

                .data(
                    this.edges
                )

                .join("line")

                .attr(
                    "stroke",
                    "#BDBDBD"
                )

                .attr(
                    "stroke-opacity",
                    0.7
                )

                .attr(

                    "stroke-width",

                    d => Math.max(

                        1,

                        d.weight ?? 1

                    )

                );

    }

    // ========================================================
    // RENDER NODES
    // ========================================================

    renderNodes() {
        this.nodeSelection =
            this.nodeLayer
                .selectAll("circle")
                .data(this.nodes)
                .join("circle")
                .attr("r", d => {
                    const degree = d.degree ?? 0;
                    d._radius = Math.max(6, 6 + degree * 20);
                    return d._radius;
                })
                .attr("fill", "#112239")
                .attr("stroke", "#FFFFFF")
                .attr("stroke-width", 1.5);
    }

    // ========================================================
    // RENDER METRIC SATELLITE NODES
    // ========================================================

    renderMetricNodes() {

        const metricDefs = [
            { key: "degree",      color: "#b91c1c", angle: -90 },
            { key: "betweenness", color: "#f5a623", angle: 30 },
            { key: "pagerank",    color: "#2ecc71", angle: 150 },
            { key: "closeness",   color: "#3b82f6", angle: 90 }
        ];

        this.metricPoints = [];

        this.nodes.forEach(parent => {
            metricDefs.forEach(m => {
                this.metricPoints.push({
                    parent,
                    key: m.key,
                    color: m.color,
                    angle: (m.angle * Math.PI) / 180,
                    distance: (parent._radius ?? 10) + 18
                });
            });
        });

        this.metricLineSelection =
            this.metricLineLayer
                .selectAll("line")
                .data(this.metricPoints)
                .join("line")
                .attr("stroke", d => d.color)
                .attr("stroke-width", 1.5)
                .attr("stroke-opacity", 0.6);

        this.metricNodeSelection =
            this.metricNodeLayer
                .selectAll("circle")
                .data(this.metricPoints)
                .join("circle")
                .attr("r", 5)
                .attr("fill", d => d.color)
                .attr("stroke", "#FFFFFF")
                .attr("stroke-width", 1);
    }
    
    // ========================================================
    // RENDER LABELS
    // ========================================================

    renderLabels() {

        this.labelSelection =

            this.labelLayer

                .selectAll("text")

                .data(
                    this.nodes
                )

                .join("text")

                .text(

                    d => d.label ?? ""

                )

                .attr(
                    "font-size",
                    11
                )

                .attr(
                    "font-family",
                    "Arial"
                )

                .attr(
                    "fill",
                    "#94a3b8"
                )

                .attr(
                    "dx",
                    10
                )

                .attr(
                    "dy",
                    4
                )
                .attr("text-anchor", "middle")

                .style(
                    "pointer-events",
                    "none"
                );

    }

    // ========================================================
    // START SIMULATION
    // ========================================================

    startSimulation() {

        this.simulation

            .nodes(
                this.nodes
            );

        this.simulation

            .force(
                "link"
            )

            .links(
                this.edges
            );

        this.simulation

            .on(

                "tick",

                () => {

                    //--------------------------------------------------
                    // EDGE
                    //--------------------------------------------------

                    this.edgeSelection

                        .attr(

                            "x1",

                            d => d.source.x

                        )

                        .attr(

                            "y1",

                            d => d.source.y

                        )

                        .attr(

                            "x2",

                            d => d.target.x

                        )

                        .attr(

                            "y2",

                            d => d.target.y

                        );
                        this.metricLineSelection
                            .attr("x1", d => d.parent.x)
                            .attr("y1", d => d.parent.y)
                            .attr("x2", d => d.parent.x + Math.cos(d.angle) * d.distance)
                            .attr("y2", d => d.parent.y + Math.sin(d.angle) * d.distance);

                        this.metricNodeSelection
                            .attr("cx", d => d.parent.x + Math.cos(d.angle) * d.distance)
                            .attr("cy", d => d.parent.y + Math.sin(d.angle) * d.distance);

                    //--------------------------------------------------
                    // NODE
                    //--------------------------------------------------

                    this.nodeSelection
                        .attr("transform", d => `translate(${d.x},${d.y})`);

                    //--------------------------------------------------
                    // RANK BADGE
                    //--------------------------------------------------

                    if (this.rankBadgeSelection) {
                        this.rankBadgeSelection
                            .attr("transform", d =>
                                `translate(${d.x + (d._radius ?? 10) * 0.7},${d.y - (d._radius ?? 10) * 0.7})`
                            );
                    }

                    //--------------------------------------------------
                    // LABEL
                    //--------------------------------------------------

                    this.labelSelection

                        .attr(

                            "x",

                            d => d.x

                        )

                        .attr(

                            "y",

                            d => d.y

                        );

                }

            );

        this.simulation

            .alpha(1)

            .restart();

    }
    // ========================================================
    // ENABLE INTERACTION
    // ========================================================

    enableInteraction() {

        // ----------------------------------------------------
        // REMOVE OLD TOOLTIP
        // ----------------------------------------------------

        d3.selectAll(".graph-tooltip").remove();

        // ----------------------------------------------------
        // CREATE TOOLTIP
        // ----------------------------------------------------

        this.tooltip = d3.select("body")

            .append("div")

            .attr("class", "graph-tooltip")

            .style("position", "absolute")

            .style("pointer-events", "none")

            .style("opacity", 0)

            .style("padding", "10px")

            .style("background", "#FFFFFF")

            .style("border", "1px solid #DDDDDD")

            .style("border-radius", "6px")

            .style("font-size", "12px")

            .style("box-shadow", "0 2px 8px rgba(0,0,0,.2)");

        // ----------------------------------------------------
        // DRAG
        // ----------------------------------------------------

        const drag = d3.drag()

            .on(

                "start",

                (event, d) => {

                    if (!event.active) {

                        this.simulation

                            .alphaTarget(0.3)

                            .restart();

                    }

                    d.fx = d.x;

                    d.fy = d.y;

                }

            )

            .on(

                "drag",

                (event, d) => {

                    d.fx = event.x;

                    d.fy = event.y;

                }

            )

            .on(

                "end",

                (event, d) => {

                    if (!event.active) {

                        this.simulation

                            .alphaTarget(0);

                    }

                    d.fx = null;

                    d.fy = null;

                }

            );

        this.nodeSelection.call(drag);

        // ----------------------------------------------------
        // TOOLTIP
        // ----------------------------------------------------

        this.nodeSelection

            .on(

                "mouseover",

                (event, d) => {

                    this.tooltip

                        .style("opacity", 1)

                        .html(
                            `
                                <strong>${d.label ?? ""}</strong>

                                <hr>

                                Số cộng tác viên:
                                ${d.collab_count ?? 0} người

                                <br>

                                Cầu nối (Betweenness):
                                ${(d.betweenness ?? 0).toFixed(4)}
                                ${d.betweenness_rank ? `(hạng #${d.betweenness_rank})` : ""}

                                <br>

                                Tốc độ tiếp cận (Closeness):
                                ${(d.closeness ?? 0).toFixed(4)}
                                ${d.closeness_rank ? `(hạng #${d.closeness_rank})` : ""}

                                <br>

                                Ảnh hưởng (PageRank):
                                ${(d.pagerank ?? 0).toFixed(4)}
                                ${d.pagerank_rank ? `(hạng #${d.pagerank_rank})` : ""}
                                `

                        );

                }

            )

            .on(

                "mousemove",

                (event) => {

                    this.tooltip

                        .style(

                            "left",

                            `${event.pageX + 12}px`

                        )

                        .style(

                            "top",

                            `${event.pageY - 20}px`

                        );

                }

            )

            .on(

                "mouseout",

                () => {

                    this.tooltip

                        .style("opacity", 0);

                }

            );

        // ----------------------------------------------------
        // CLICK NODE
        // ----------------------------------------------------

        this.nodeSelection.on(

            "click",

            (event, d) => {

                event.stopPropagation();

                this.highlightNeighbors(

                    d.id

                );

            }

        );

        // ----------------------------------------------------
        // CLICK BACKGROUND
        // ----------------------------------------------------

        this.svg.on(

            "click",

            () => {

                this.resetHighlight();

            }

        );

    }

    // ========================================================
    // HIGHLIGHT NEIGHBORS
    // ========================================================

    highlightNeighbors(nodeId) {

        const connected = new Set();

        connected.add(nodeId);

        this.edges.forEach(

            (edge) => {

                const source =

                    edge.source.id ??

                    edge.source;

                const target =

                    edge.target.id ??

                    edge.target;

                if (source === nodeId) {

                    connected.add(target);

                }

                if (target === nodeId) {

                    connected.add(source);

                }

            }

        );

        this.nodeSelection

            .attr(

                "opacity",

                d => connected.has(d.id)

                    ? 1

                    : 0.15

            );

        this.labelSelection

            .attr(

                "opacity",

                d => connected.has(d.id)

                    ? 1

                    : 0.15

            );

        this.edgeSelection

            .attr(

                "opacity",

                d => {

                    const source =

                        d.source.id ??

                        d.source;

                    const target =

                        d.target.id ??

                        d.target;

                    if (

                        source === nodeId ||

                        target === nodeId

                    ) {

                        return 1;

                    }

                    return 0.08;

                }

            );

    }

    // ========================================================
    // RESET HIGHLIGHT
    // ========================================================

    resetHighlight() {

        this.nodeSelection

            .attr(

                "opacity",

                1

            );

        this.edgeSelection

            .attr(

                "opacity",

                1

            );

        this.labelSelection

            .attr(

                "opacity",

                1

            );

    }

    // ========================================================
    // HIGHLIGHT TOP BRIDGES (top betweenness)
    // ========================================================

    highlightTopBridges(topN = 3) {

        const bridgeIds = new Set(
            this.nodes
                .filter(d => (d.betweenness_rank ?? Infinity) <= topN)
                .map(d => d.id)
        );

        this.nodeSelection
            .attr("stroke", d => bridgeIds.has(d.id) ? "#f5a623" : "#FFFFFF")
            .attr("stroke-width", d => bridgeIds.has(d.id) ? 3 : 1.5);

        // ----------------------------------------------------
        // BADGE HẠNG (1, 2, 3)
        // ----------------------------------------------------

        if (!this.rankBadgeLayer) {
            this.rankBadgeLayer = this.container
                .append("g")
                .attr("class", "rank-badge-layer");
        }

        const bridgeNodes = this.nodes.filter(
            d => (d.betweenness_rank ?? Infinity) <= topN
        );

        const rankColors = {
            1: "#f5a623", // vàng
            2: "#94a3b8", // bạc
            3: "#b87333"  // đồng
        };

        this.rankBadgeSelection = this.rankBadgeLayer
            .selectAll("g.rank-badge")
            .data(bridgeNodes, d => d.id)
            .join(
                enter => {
                    const g = enter.append("g").attr("class", "rank-badge");
                    g.append("circle")
                        .attr("r", 9)
                        .attr("stroke", "#FFFFFF")
                        .attr("stroke-width", 1.5);
                    g.append("text")
                        .attr("text-anchor", "middle")
                        .attr("dy", 4)
                        .attr("font-size", 10)
                        .attr("font-weight", "bold")
                        .attr("fill", "#FFFFFF")
                        .style("pointer-events", "none");
                    return g;
                }
            );

        this.rankBadgeSelection.select("circle")
            .attr("fill", d => rankColors[d.betweenness_rank] ?? "#f5a623");

        this.rankBadgeSelection.select("text")
            .text(d => d.betweenness_rank);

    }

    // ========================================================
    // UPDATE GRAPH
    //
    // Dùng khi backend trả graph mới
    // (Filter Year / Filter Topic)
    // ========================================================

    updateGraph(graphData) {

        this.nodes = graphData.nodes || [];

        this.edges = graphData.edges || [];

        this.render();

        this.highlightTopBridges(3);

    }

    // ========================================================
    // RESET ZOOM
    // ========================================================

    resetZoom() {

        this.svg

            .transition()

            .duration(500)

            .call(

                this.zoom.transform,

                d3.zoomIdentity

            );

    }

    // ========================================================
    // DESTROY GRAPH
    //
    // Dừng simulation khi không còn sử dụng.
    // ========================================================

    destroy() {

        if (this.simulation) {

            this.simulation.stop();

        }

        this.edgeLayer.selectAll("*").remove();

        this.nodeLayer.selectAll("*").remove();

        this.labelLayer.selectAll("*").remove();

        if (this.tooltip) {

            this.tooltip.remove();

            this.tooltip = null;

        }

    }

    // ========================================================
    // GET GRAPH DATA
    // ========================================================

    getGraphData() {

        return {

            nodes: this.nodes,

            edges: this.edges

        };

    }

    // ========================================================
    // GRAPH STATISTICS
    // ========================================================

    getStatistics() {

        return {

            totalNodes: this.nodes.length,

            totalEdges: this.edges.length

        };

    }

    // ========================================================
    // EXPORT JSON
    // ========================================================

    exportJSON() {

        return JSON.stringify(

            {

                nodes: this.nodes,

                edges: this.edges

            },

            null,

            4

        );

    }

    // ========================================================
    // DOUBLE CLICK
    //
    // Reset zoom về mặc định.
    // ========================================================

    enableDoubleClickReset() {

        this.svg.on(

            "dblclick",

            () => {

                this.resetZoom();

            }

        );

    }
}
export default CollaborationGraph;