// ======================================================
// DOM
// ======================================================

const badge = document.querySelector(".badge-paper");

const year = document.querySelector(".meta-date");

const title = document.querySelector(".paper-title");

const statValues = document.querySelectorAll(".stat-value");

const statLabels = document.querySelectorAll(".stat-label");

const abstractSection = document.querySelector(".abstract-section");

const abstractText = document.querySelector(".abstract-section p");


// ======================================================
// NODE EVENT
// ======================================================

document.addEventListener(

    "nodeSelected",

    function(event){

        const {

            id,

            type

        } = event.detail;

         document.getElementById(
            "node-placeholder"
        ).style.display = "flex";

        document.getElementById(
            "node-detail-content"
        ).style.display = "none";

        loadNodeDetail(

            id,

            type

        );

    }

);

// ======================================================
// AUTHOR CHANGED — RESET DETAIL PANEL
// ======================================================

document.addEventListener(

    "authorSelected",

    function(event){

        resetDetail();

    }

);


// ======================================================
// LOAD NODE DETAIL
// ======================================================

async function loadNodeDetail(

    nodeId,

    nodeType

){

    try{

        const response = await fetch(

            `/knowledge_graph/api/knowledge_graph/node_detail?node_id=${nodeId}&node_type=${nodeType}`

        );

        if(!response.ok){

            throw new Error("Cannot load node detail.");

        }

        const data = await response.json();

        document.getElementById(
            "node-placeholder"
        ).style.display = "none";

        document.getElementById(
            "node-detail-content"
        ).style.display = "block";

        renderNode(

            nodeType,

            data

        );

    }

    catch(error){

        console.error(error);

    }

}


// ======================================================
// RENDER
// ======================================================

function renderNode(

    nodeType,

    data

){

    switch(nodeType){

        case "Author":

            renderAuthor(data);

            break;

        case "Paper":

            renderPaper(data);

            break;

        case "Topic":

            renderTopic(data);

            break;

        case "Institution":

            renderInstitution(data);

            break;

    }

}
// ======================================================
// AUTHOR
// ======================================================

function renderAuthor(data){

    // Badge
    badge.textContent = "Author";

    badge.className = "badge-paper";

    // Không có năm
    year.style.display = "none";

    // Tên tác giả
    title.textContent = data.author_name;

    document.querySelector(".stats-box").style.display = "flex";

    // Stats
    statValues[0].textContent = data.total_papers;
    statLabels[0].textContent = "PAPERS";

    statValues[1].textContent = data.total_citations;
    statLabels[1].textContent = "CITATIONS";

    // Author không có abstract
    abstractSection.style.display = "none";

}
// ======================================================
// PAPER
// ======================================================

function renderPaper(data){

    // Badge
    badge.textContent = "Paper";

    badge.className = "badge-paper";

    // Hiện năm
    year.style.display = "flex";

    // Nếu meta-date có icon SVG thì chỉ thay text phía sau
    const textNode = year.childNodes[year.childNodes.length - 1];

    if(textNode.nodeType === Node.TEXT_NODE){

        textNode.textContent = ` ${data.year}`;

    }else{

        year.append(` ${data.year}`);

    }

    // Title
    title.textContent = data.title;

    document.querySelector(".stats-box").style.display = "flex";

    // Stats
    statValues[0].textContent = data.citation_count;
    statLabels[0].textContent = "CITATIONS";

    statValues[1].textContent = data.total_authors;
    statLabels[1].textContent = "AUTHORS";

    // Abstract
    abstractSection.style.display = "block";

    abstractText.textContent =

        data.abstract || "No abstract available.";

}
// ======================================================
// TOPIC
// ======================================================

function renderTopic(data){

    // Badge
    badge.textContent = "Topic";

    badge.className = "badge-paper";

    // Không có năm
    year.style.display = "none";

    // Tên topic
    title.textContent = data.topic_name;

    // Ẩn thống kê
    document.querySelector(".stats-box").style.display = "none";

    // Ẩn abstract
    abstractSection.style.display = "none";

}


// ======================================================
// INSTITUTION
// ======================================================

function renderInstitution(data){

    // Badge
    badge.textContent = "Institution";

    badge.className = "badge-paper";

    // Không có năm
    year.style.display = "none";

    // Tên institution
    title.textContent = data.institution_name;

    // Hiện stats
    document.querySelector(".stats-box").style.display = "flex";

    // Chỉ dùng stat đầu tiên
    statValues[0].textContent = data.total_authors;
    statLabels[0].textContent = "AUTHORS";

    // Ẩn stat thứ hai
    statValues[1].textContent = "-";
    statLabels[1].textContent = "";

    // Không có abstract
    abstractSection.style.display = "none";

}


// ======================================================
// RESET DETAIL
// ======================================================

function resetDetail(){

    badge.textContent = "";

    title.textContent = "";

    year.style.display = "none";

    document.querySelector(".stats-box").style.display = "none";

    abstractSection.style.display = "none";

    document.getElementById("node-placeholder").style.display = "flex";
    
    document.getElementById("node-detail-content").style.display = "none";

}