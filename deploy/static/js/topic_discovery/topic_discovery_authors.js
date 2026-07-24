// ==========================================================
// Topic Discovery Authors
// ==========================================================

function renderTopAuthors(
    authors,
    topicName = ""
) {

    //--------------------------------------------------------
    // Title
    //--------------------------------------------------------

    const title =

        document.getElementById(
            "top_authors_title"
        );

    if (topicName) {

        title.textContent =

            `Top Authors in ${topicName}`;

    }

    else {

        title.textContent =

            "Top Authors";

    }

    //--------------------------------------------------------
    // Container
    //--------------------------------------------------------

    const container =

        document.getElementById(
            "top_authors_list"
        );

    container.innerHTML = "";

    if (
        !authors ||
        authors.length === 0
    ) {

        container.innerHTML =

            `<p>No authors found.</p>`;

        return;

    }

    //--------------------------------------------------------
    // Render
    //--------------------------------------------------------

    authors.forEach(author => {

        const avatar =

            createAvatar(

                author.author_name

            );

        container.innerHTML += `

        <div class="author-item">

            <div class="author-left">

                <div class="avatar">

                    ${avatar}

                </div>

                <div class="author-info">

                    <span class="author-name">

                        ${author.author_name}

                    </span>

                    <span class="author-papers">

                        ${formatPaper(author.paper_count)}

                    </span>

                </div>

            </div>

            <span class="author-citations">

                ${formatCitation(author.citation_count)}

            </span>

        </div>

        `;

    });

}


// ==========================================================
// Avatar
// ==========================================================

function createAvatar(name) {

    if (!name) {

        return "--";

    }

    const words =

        name

        .trim()

        .split(/\s+/);

    if (words.length === 1) {

        return words[0]

            .substring(0,2)

            .toUpperCase();

    }

    return (

        words[0][0] +

        words[words.length-1][0]

    ).toUpperCase();

}


// ==========================================================
// Paper Text
// ==========================================================

function formatPaper(value) {

    if (value === 1) {

        return "1 paper";

    }

    return `${Number(value).toLocaleString()} papers`;

}


// ==========================================================
// Citation Text
// ==========================================================

function formatCitation(value) {

    return `${Number(value).toLocaleString()} cit.`;

}