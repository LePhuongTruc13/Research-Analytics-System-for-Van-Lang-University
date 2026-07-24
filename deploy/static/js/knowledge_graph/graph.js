// ======================================================
// GRAPH CONFIG
// ======================================================

const Graph = {

    svg: null,

    g: null,

    simulation: null,

    width: 0,

    height: 0,

};


// ======================================================
// INITIALIZE GRAPH
// ======================================================

function initGraph(){

    const container = document.getElementById(
        "network-graph"
    );

    Graph.width = container.clientWidth;

    Graph.height = container.clientHeight;

    // Remove old graph

    d3.select("#network-graph")
        .selectAll("*")
        .remove();

    // SVG

    Graph.svg = d3
        .select("#network-graph")
        .append("svg")
        .attr("width", Graph.width)
        .attr("height", Graph.height);

    // Group

    Graph.g = Graph.svg
        .append("g");

    // Zoom

    enableZoom();

    // Force Simulation

    createSimulation();

    Graph.svg.on("click", function(){
        resetHighlight();
    });

}


// ======================================================
// FORCE SIMULATION
// ======================================================

function createSimulation(){

    Graph.simulation = d3.forceSimulation()

        .force(

            "link",

            d3.forceLink()

                .id(d=>d.id)

                .distance(140)

        )

        .force(

            "charge",

            d3.forceManyBody()

                .strength(-700)

        )

        .force(

            "center",

            d3.forceCenter(

                Graph.width / 2,

                Graph.height / 2

            )

        )

        .force(

            "collision",

            d3.forceCollide(

                35

            )

        );

}


// ======================================================
// ENABLE ZOOM
// ======================================================

function enableZoom(){

    const zoom = d3.zoom()

        .scaleExtent([0.3,5])

        .on(

            "zoom",

            function(event){

                Graph.g.attr(

                    "transform",

                    event.transform

                );

            }

        );

    Graph.svg.call(

        zoom

    );

}


// ======================================================
// RESIZE GRAPH
// ======================================================

window.addEventListener(

    "resize",

    function(){

        const container = document.getElementById(
            "network-graph"
        );

        Graph.width = container.clientWidth;

        Graph.height = container.clientHeight;

        Graph.svg
            .attr(
                "width",
                Graph.width
            )
            .attr(
                "height",
                Graph.height
            );

        Graph.simulation.force(

            "center",

            d3.forceCenter(

                Graph.width/2,

                Graph.height/2

            )

        );

        Graph.simulation.alpha(1).restart();

    }

);


// ======================================================
// INITIALIZE
// ======================================================

initGraph();
// ======================================================
// LOAD GRAPH
// ======================================================

async function loadGraph(authorId){

    try{

        const response = await fetch(

            `/knowledge_graph/api/knowledge_graph/graph?author_id=${authorId}` 

        );

        const graph = await response.json();

        renderGraph(graph);

    }

    catch(error){

        console.error(error);

    }

}


// ======================================================
// RENDER GRAPH
// ======================================================

function renderGraph(graph){

    Graph.g.selectAll("*").remove();

    drawLinks(graph.edges);

    drawNodes(graph.nodes);

    drawLabels(graph.nodes);

    enableDrag(Graph.nodes);        
    enableNodeClick(Graph.nodes);   

    Graph.simulation

        .nodes(graph.nodes)

        .on("tick", ticked);

    Graph.simulation

        .force("link")

        .links(graph.edges);

    Graph.simulation

        .alpha(1)

        .restart();

}


// ======================================================
// DRAW LINKS
// ======================================================

function drawLinks(edges){

    Graph.links = Graph.g

        .append("g")

        .attr("class","links")

        .selectAll("line")

        .data(edges)

        .enter()

        .append("line")

        .attr("stroke","#bdbdbd")

        .attr("stroke-width",1.6)

        .attr("opacity",0.8);

}


// ======================================================
// DRAW NODES
// ======================================================

function drawNodes(nodes){

    Graph.nodes = Graph.g

        .append("g")

        .attr("class","nodes")

        .selectAll("circle")

        .data(nodes)

        .enter()

        .append("circle")

        .attr("r",function(d){

            switch(d.type){

                case "Author":

                    return 18;

                case "Paper":

                    return 14;

                case "Topic":

                    return 10;

                case "Institution":

                    return 9;

                default:

                    return 10;

            }

        })

        .attr("fill",function(d){

            switch(d.type){

                case "Author":

                    return "#112239";

                case "Paper":

                    return "#3b82f6";

                case "Topic":

                    return "#2ecc71";

                case "Institution":

                    return "#f5a623";

                default:

                    return "#999";

            }

        });

}


// ======================================================
// DRAW LABELS
// ======================================================

function drawLabels(nodes){

    Graph.labels = Graph.g

        .append("g")

        .attr("class","labels")

        .selectAll("text")

        .data(nodes)

        .enter()

        .append("text")

        .text(d=>d.label)

        .attr("font-size",11)

        .attr("font-family","Inter")

        .attr("fill","#94a3b8")

        .attr("dx",15)

        .attr("dy",4);

}


// ======================================================
// TICK
// ======================================================

function ticked(){

    Graph.links

        .attr("x1",d=>d.source.x)

        .attr("y1",d=>d.source.y)

        .attr("x2",d=>d.target.x)

        .attr("y2",d=>d.target.y);

    Graph.nodes

        .attr("cx",d=>d.x)

        .attr("cy",d=>d.y);

    Graph.labels

        .attr("x",d=>d.x)

        .attr("y",d=>d.y);

}


// ======================================================
// ENABLE DRAG
// ======================================================

function enableDrag(nodes){

    nodes.call(

        d3.drag()

            .on("start", dragStarted)

            .on("drag", dragged)

            .on("end", dragEnded)

    );

}

function dragStarted(event,d){

    if(!event.active){

        Graph.simulation.alphaTarget(0.3).restart();

    }

    d.fx = d.x;

    d.fy = d.y;

}

function dragged(event,d){

    d.fx = event.x;

    d.fy = event.y;

}

function dragEnded(event,d){

    if(!event.active){

        Graph.simulation.alphaTarget(0);

    }

    d.fx = null;

    d.fy = null;

}


// ======================================================
// ENABLE NODE CLICK
// ======================================================

function enableNodeClick(nodes){

    nodes.on(

        "click",

        function(event,node){

            event.stopPropagation();

            highlightNeighbors(node);

            dispatchNodeEvent(node);

        }

    );

}


// ======================================================
// HIGHLIGHT
// ======================================================

function highlightNeighbors(selected){

    if(!Graph.nodes || !Graph.links || !Graph.labels) return;
    
    const connected = new Set();

    connected.add(selected.id);

    Graph.links.each(function(edge){

        const sourceId =

            typeof edge.source === "object"

                ? edge.source.id

                : edge.source;

        const targetId =

            typeof edge.target === "object"

                ? edge.target.id

                : edge.target;

        if(

            sourceId === selected.id ||

            targetId === selected.id

        ){

            connected.add(sourceId);

            connected.add(targetId);

        }

    });

    // ----------------------------

    // Node opacity

    Graph.nodes

        .attr(

            "opacity",

            d=>connected.has(d.id)

                ? 1

                : 0.15

        );

    // ----------------------------

    // Label opacity

    Graph.labels

        .attr(

            "opacity",

            d=>connected.has(d.id)

                ? 1

                : 0.15

        );

    // ----------------------------

    // Edge opacity

    Graph.links

        .attr(

            "opacity",

            function(edge){

                const sourceId =

                    typeof edge.source === "object"

                        ? edge.source.id

                        : edge.source;

                const targetId =

                    typeof edge.target === "object"

                        ? edge.target.id

                        : edge.target;

                if(

                    sourceId === selected.id ||

                    targetId === selected.id

                ){

                    return 1;

                }

                return 0.08;

            }

        )

        .attr(

            "stroke-width",

            function(edge){

                const sourceId =

                    typeof edge.source === "object"

                        ? edge.source.id

                        : edge.source;

                const targetId =

                    typeof edge.target === "object"

                        ? edge.target.id

                        : edge.target;

                if(

                    sourceId === selected.id ||

                    targetId === selected.id

                ){

                    return 3;

                }

                return 1.2;

            }

        );

}


// ======================================================
// RESET
// ======================================================

function resetHighlight(){

    if(!Graph.nodes || !Graph.links || !Graph.labels) return;

    Graph.nodes

        .attr("opacity",1);

    Graph.labels

        .attr("opacity",1);

    Graph.links

        .attr("opacity",0.8)

        .attr("stroke-width",1.6);

}


// ======================================================
// NODE EVENT
// ======================================================

function dispatchNodeEvent(node){

    document.dispatchEvent(

        new CustomEvent(

            "nodeSelected",

            {

                detail:{

                    id:node.id,

                    type:node.type,

                    label:node.label

                }

            }

        )

    );

}
// ======================================================
// AUTHOR FILTER EVENT
// ======================================================

document.addEventListener(

    "authorSelected",

    function(event){

        const authorId = event.detail.author_id;

        loadGraph(authorId);

    }

);


// ======================================================
// NODE DETAIL EVENT
// ======================================================

document.addEventListener(

    "nodeSelected",

    function(event){

        console.log(

            "Selected Node :",

            event.detail

        );

    }

);


// ======================================================
// INITIAL GRAPH
// ======================================================

window.addEventListener(

    "DOMContentLoaded",

    function(){

        initGraph();

    }

);


// ======================================================
// OPTIONAL
// Load first author automatically
// ======================================================

document.addEventListener(

    "DOMContentLoaded",

    function(){

        if(

            window.AuthorFilter &&

            AuthorFilter.getSelectedAuthor()

        ){

            loadGraph(

                AuthorFilter.getSelectedAuthor()

            );

        }

    }

);
