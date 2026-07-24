// ==========================================================
// Dashboard Summary Cards
// ==========================================================

function renderSummaryCards(cards) {

    renderTotalPapers(cards.total_papers);

    renderTotalAuthors(cards.total_authors);

    renderTotalCitations(cards.total_citations);

    renderTotalTopics(cards.total_topics);

    renderInternationalCollaboration(
        cards.international_collaboration
    );

    renderAveragePagerank(
        cards.average_pagerank
    );

}


// ==========================================================
// Total Papers
// ==========================================================

function renderTotalPapers(value) {

    document.getElementById(
        "total_papers"
    ).textContent = value.toLocaleString();

}


// ==========================================================
// Total Authors
// ==========================================================

function renderTotalAuthors(value) {

    document.getElementById(
        "total_authors"
    ).textContent = value.toLocaleString();

}


// ==========================================================
// Total Citations
// ==========================================================

function renderTotalCitations(value) {

    document.getElementById(
        "total_citations"
    ).textContent = value.toLocaleString();

}


// ==========================================================
// Total Topics
// ==========================================================

function renderTotalTopics(value) {

    document.getElementById(
        "total_topics"
    ).textContent = value.toLocaleString();

}


// ==========================================================
// International Collaboration
// ==========================================================

function renderInternationalCollaboration(value) {

    document.getElementById(
        "international_collaboration"
    ).textContent = value.toLocaleString();

}


// ==========================================================
// Average PageRank
// ==========================================================

function renderAveragePagerank(value) {

    document.getElementById(
        "average_pagerank"
    ).textContent = Number(value).toFixed(6);

}