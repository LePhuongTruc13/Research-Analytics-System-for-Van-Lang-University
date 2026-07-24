// ==========================================================
// Topic Discovery Cards
// ==========================================================

function renderTopicSummary(summary) {

    if (!summary) return;

    // ------------------------------------------------------
    // Papers
    // ------------------------------------------------------

    document.getElementById(
        "topic_papers"
    ).textContent = formatNumber(
        summary.papers
    );

    // ------------------------------------------------------
    // Authors
    // ------------------------------------------------------

    document.getElementById(
        "topic_authors"
    ).textContent = formatNumber(
        summary.authors
    );

    // ------------------------------------------------------
    // Citations
    // ------------------------------------------------------

    document.getElementById(
        "topic_citations"
    ).textContent = formatNumber(
        summary.citations
    );

    // ------------------------------------------------------
    // Average PageRank
    // ------------------------------------------------------

    document.getElementById(
        "topic_pagerank"
    ).textContent = Number(
        summary.average_pagerank
    ).toFixed(6);

}


// ==========================================================
// Number Formatter
// ==========================================================

function formatNumber(value) {

    if (
        value === null ||
        value === undefined
    ) {

        return "0";

    }

    return Number(value).toLocaleString();

}