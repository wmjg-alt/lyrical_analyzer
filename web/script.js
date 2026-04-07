const app = { svg: null, mainGroup: null, simulation: null, links: null, nodes: null, labels: null };
const config = { repulsion: -25, 
    linkDistance: 75, 
    zoomMin: 0.1, 
    zoomMax: 4 };

function getNodeColor(type) {
    const colors = { topic: "#e91e63", word: "#2196f3", song: "#4caf50" };
    return colors[type] || "#ffffff";
}

function getNodeRadius(type) {
    const sizes = { topic: 15, word: 8, song: 5 };
    return sizes[type] || 5;
}

function setupZoom() {
    const zoom = d3.zoom().scaleExtent([config.zoomMin, config.zoomMax])
        .on("zoom", (e) => app.mainGroup.attr("transform", e.transform));
    app.svg.call(zoom);
}

function createSVG() {
    d3.select("#graph-container").select("svg").remove();
    app.svg = d3.select("#graph-container").append("svg")
        .attr("width", window.innerWidth)
        .attr("height", window.innerHeight - 50);
    app.mainGroup = app.svg.append("g");
    setupZoom();
}

function dragstarted(event, d) {
    if (!event.active) app.simulation.alphaTarget(0.3).restart();
    d.fx = d.x; d.fy = d.y;
}

function dragged(event, d) { d.fx = event.x; d.fy = event.y; }

function dragended(event, d) {
    if (!event.active) app.simulation.alphaTarget(0);
    d.fx = null; d.fy = null;
}

function getDragBehavior() {
    return d3.drag().on("start", dragstarted).on("drag", dragged).on("end", dragended);
}

function initSimulation(graphData) {
    app.simulation = d3.forceSimulation(graphData.nodes)
        .force("link", d3.forceLink(graphData.links).id(d => d.id).distance(config.linkDistance))
        .force("charge", d3.forceManyBody().strength(config.repulsion))
        .force("center", d3.forceCenter(window.innerWidth / 2, window.innerHeight / 2));
}

function drawLinks(linksData) {
    app.links = app.mainGroup.append("g").selectAll("line")
        .data(linksData).enter().append("line")
        .attr("stroke", "#555")
        .attr("stroke-width", d => Math.sqrt(d.weight));
}

function drawNodes(nodesData) {
    app.nodes = app.mainGroup.append("g").selectAll("circle")
        .data(nodesData).enter().append("circle")
        .attr("r", d => getNodeRadius(d.type))
        .attr("fill", d => getNodeColor(d.type))
        .call(getDragBehavior())
        .on("click", (event, d) => highlightConnections(d));
}

function drawLabels(nodesData) {
    app.labels = app.mainGroup.append("g").selectAll("text")
        .data(nodesData).enter().append("text")
        .attr("class", "node-label")
        .text(d => d.type === 'song' ? '' : d.id)
        .attr("dx", 12).attr("dy", 4);
}

function setSimulationTicks() {
    app.simulation.on("tick", () => {
        app.links.attr("x1", d => d.source.x).attr("y1", d => d.source.y)
            .attr("x2", d => d.target.x).attr("y2", d => d.target.y);
        app.nodes.attr("cx", d => d.x).attr("cy", d => d.y);
        app.labels.attr("x", d => d.x).attr("y", d => d.y);
    });
}

function highlightConnections(selectedNode) {
    const connected = new Set([selectedNode.id]);
    app.links.each(d => {
        if (d.source.id === selectedNode.id) connected.add(d.target.id);
        if (d.target.id === selectedNode.id) connected.add(d.source.id);
    });
    app.nodes.classed("dimmed", d => !connected.has(d.id));
    app.links.classed("dimmed", d => !connected.has(d.source.id) && !connected.has(d.target.id));
    app.labels.classed("dimmed", d => !connected.has(d.id));
}

app.resetHighlight = () => {
    app.nodes.classed("dimmed", false);
    app.links.classed("dimmed", false);
    app.labels.classed("dimmed", false);
};

app.searchNode = () => {
    const term = document.getElementById("searchInput").value.toLowerCase();
    const target = app.nodes.data().find(d => d.id.toLowerCase().includes(term));
    if (target) highlightConnections(target);
};

app.loadBand = async () => {
    const band = document.getElementById("bandSelect").value;
    const res = await fetch(`./export/${band}_network.json`);
    const data = await res.json();
    createSVG();
    drawLinks(data.links);
    drawNodes(data.nodes);
    drawLabels(data.labels || data.nodes); // Handle potential data structure difference
    initSimulation(data);
    setSimulationTicks();
};


async function initApp() {
    const res = await fetch(`./export/manifest.json`);
    const bands = await res.json();
    const select = document.getElementById("bandSelect");
    
    // Clear existing options first
    select.innerHTML = ''; 
    
    bands.forEach(b => { select.add(new Option(b.replace(/_/g, ' '), b)); });
    
    document.getElementById("searchInput").addEventListener("keypress", e => {
        if (e.key === "Enter") app.searchNode();
    });
    
    if (bands.length > 0) app.loadBand();
}

window.onload = initApp;