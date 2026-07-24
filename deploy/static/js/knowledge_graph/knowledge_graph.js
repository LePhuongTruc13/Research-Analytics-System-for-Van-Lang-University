// ======================================================
// KNOWLEDGE GRAPH CONTROLLER
// ======================================================

document.addEventListener(
    "DOMContentLoaded",
    initializeKnowledgeGraph
);

// ======================================================
// Initialize
// ======================================================

async function initializeKnowledgeGraph() {

    try {

        const authors = await loadAuthors();

        AuthorFilter.init(authors);

        if (authors.length > 0) {

            const randomAuthor =
                authors[Math.floor(Math.random() * authors.length)];

            AuthorFilter.selectRandom(randomAuthor);

        }


    }
    catch (error) {

        console.error(error);

    }

}

// ======================================================
// Load Authors
// ======================================================

async function loadAuthors() {

    const response = await fetch(
        "/knowledge_graph/api/knowledge_graph/authors"
    );

    if (!response.ok) {

        throw new Error(
            "Cannot load author list."
        );

    }

    return await response.json();

}

