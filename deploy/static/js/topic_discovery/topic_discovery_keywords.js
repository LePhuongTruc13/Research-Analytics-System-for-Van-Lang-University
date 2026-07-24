// ==========================================================
// Topic Discovery Keywords
// ==========================================================

function renderTopicKeywords(keywords) {

    //--------------------------------------------------------
    // Container
    //--------------------------------------------------------

    const container =

        document.getElementById(
            "topic_keywords"
        );

    container.innerHTML = "";

    if (
        !keywords ||
        keywords.length === 0
    ) {

        container.innerHTML =
            "<span>No keywords</span>";

        return;

    }

    //--------------------------------------------------------
    // Keyword Size Class
    //--------------------------------------------------------

    keywords.forEach((keyword, index) => {

        let cls = "kw-xs";

        if (index < 3) {

            cls = "kw-xl";

        }

        else if (index < 5) {

            cls = "kw-md";

        }

        else if (index < 8) {

            cls = "kw-sm";

        }

        container.innerHTML += `

            <span class="${cls}">

                ${keyword}

            </span>

        `;

    });

}